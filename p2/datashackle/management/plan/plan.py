# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok

from grokcore.content.interfaces import IContext
from sqlalchemy import orm
from zope.app.appsetup.product import getProductConfiguration
from zope.component import getUtility, queryUtility
from zope.location.interfaces import ILocation

from p2.datashackle.core import model_config
from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.core.models.model import StrippedModel
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.management.form.form import FormType, FormTypeFactory
from p2.datashackle.management.widget.widget import WidgetType
from p2.datashackle.management.span.span import SpanType
from p2.datashackle.management.interfaces import IModel, ILocationProvider

        
def fetch_plan(genericset):
    db_util = getUtility(IDbUtility)
    session = db_util.Session()
    plan = session.query(Model).filter_by(plan_identifier=genericset.plan_identifier).one()
    session.add(plan)
    plan.make_locatable(genericset.__name__, genericset.__parent__)
    return plan
               

@model_config()
class Model(StrippedModel):
    # In order to find default views via /index rather than
    # Zope3's /index.html we need to implement interfaces.IContext
    grok.implements(IModel, IContext, ILocation)
 
    def __init__(self):
        super(Model, self).__init__()

        form = FormTypeFactory.copy(plan_name='p2_archetype', form_name='default_form')
        self.forms['default_form'] = form        
        self.default_form = form
        
    @orm.reconstructor          
    def reconstruct(self):
        util = getUtility(ILocationProvider)
        genericset = util.get_genericset(self.plan_identifier)

        if genericset != None:
            self.make_locatable(genericset.__name__, genericset.__parent__)
        super(Model, self).reconstruct()
    
    def common_init(self):
        super(Model, self).common_init()
        self.form_type = FormType.__name__
        self.form_module = FormType.__module__

    def make_locatable(self, name, parent):
         # Implementation of ILocation interface enables the object to be located with an URL,
         # which is needed for views of the plan, form and the like.
         self.__name__ = name
         self.__parent__ = parent

    @classmethod
    def map_computed_properties(cls):
        orm.mapper(cls,
                 inherits=StrippedModel._sa_class_manager.mapper,
                 properties=cls.mapper_properties,
                 )

    def traverse(self, name):
        if name == 'forms':
            return FormDirectory(self)
        elif name == 'default_form':
            return self.default_form
    
    def is_archetype(self):
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
        return self.context.forms[name]

