# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
import logging
import os
import types

from grokcore.content.interfaces import IContext
from sqlalchemy import orm
from zope.app.appsetup.product import getProductConfiguration
from zope.component import getUtility, queryUtility
from zope.location.interfaces import ILocation

from p2.datashackle.core import model_config
from p2.datashackle.core.app.exceptions import *
from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.core.models.model import Model
from p2.datashackle.core.interfaces import ILocationProvider, IDbUtility 
from p2.datashackle.management.form.form import FormType
from p2.datashackle.management.widget.widget import WidgetType
from p2.datashackle.management.span.span import SpanType
from p2.datashackle.management.interfaces import IPlan

        
def fetch_plan(genericset):
    db_util = getUtility(IDbUtility)
    session = db_util.Session()
    plan = session.query(Plan).filter_by(plan_identifier=genericset.plan_identifier).one()
    session.add(plan)
    plan.make_locatable(genericset.__name__, genericset.__parent__)
    return plan

@model_config()
class Plan(Model):
    # In order to find default views via /index rather than
    # Zope3's /index.html we need to implement interfaces.IContext
    grok.implements(IPlan, IContext, ILocation)
 
    def __init__(self, id, klass, table):
        self.id = id
        self.table = table
        self.klass = klass
        self.forms = dict()
        
        #util = getUtility(ILocationProvider)
        #genericset = util.get_genericset(objid)
        #self.table_identifier = genericset.table_identifier
        super(Plan, self).__init__()
     
    @orm.reconstructor          
    def reconstruct(self):
        util = getUtility(ILocationProvider)
        genericset = util.get_genericset(self.plan_identifier) # Requires that genericset.plan_identifier
                                                               # (yes, genericset.plan_identifier, not self.plan_identifier)
        if genericset != None:
            self.make_locatable(genericset.__name__, genericset.__parent__)
        super(Plan, self).reconstruct()
    
    def common_init(self):
        super(Plan, self).common_init()
        self.form_type = FormType.__name__
        self.form_module = FormType.__module__

    def is_operating_on_sys_table(self):
        return self.table_identifier.startswith('p2_')

    def set_default(self, form):
        self.default_form = form

    def make_locatable(self, name, parent):
         # Implementation of ILocation interface enables the object to be located with an URL,
         # which is needed for views of the plan, form and the like.
         self.__name__ = name
         self.__parent__ = parent
                 
    def register_form(self, form):
        if not form.form_name in self.forms:
            self.forms[form.form_name] = form
           
    def traverse(self, name):
        if name == 'forms':
            return FormDirectory(self)
        elif name == 'default_form':
            return self.default_form
    
    def is_archetype(self):
        """ Check whether we are an archetype plan."""
        if self.plan_identifier == 'p2_archetype':
            return True
        return False

    @property
    def table_identifier(self):
        """The table on which this plan is operating."""
        klass = setobject_type_registry.lookup(self.klass)
        return klass.get_table_name()
 
 

class FormDirectory(object):
    def __init__(self, plan):
        self.plan = plan
        self.forms = plan.forms


class FormTraverser(grok.Traverser):
    grok.context(FormDirectory)

    def traverse(self, name):
        if name in self.context.forms:
            return self.context.forms[name]
        raise Exception("Form does not exist.")

