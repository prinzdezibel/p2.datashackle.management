# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
import logging

from sqlalchemy import orm
from sqlalchemy.orm import exc
from grokcore.content import interfaces
from zope.component import getUtility, getMultiAdapter
from zope.location.interfaces import ILocation

from p2.datashackle.core import model_config
from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.core.models.setobject_types import SetobjectType
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.management.setobject_graph import SetobjectGraph
from p2.datashackle.management.widget.widget_factory import create_widget
from p2.datashackle.management.interfaces import IFormType



class LocationHelper(object):
    grok.implements(ILocation)
    def __init__(self, parent):
        self.__parent__ = parent
        self.__name__ = 'forms'

@model_config(maporder=2)
class FormType(SetobjectType):
    # In order to find default views via /index rather than
    # Zope3's /index.html we need to implement interfaces.IContext
    # The form gains location awareness (grok.url() capability) through implementing ILocation
    grok.implements(IFormType, interfaces.IContext, ILocation)

    def __init__(self, form_name=None, plan=None):
        # BEGIN sqlalchemy instrumented attributes
        # self.form_identifier initialized through SetobjectType base class.
        self.plan = plan
        self.form_name = form_name
        self.widgets = dict()
        self.css = 'height:300px; width:400px;'
        self.fk_formlayout = 'FORM'
        # END sqlalchemy instrumented attributes
 
        if self.plan != None:    
            self.plan_identifier = plan.id
            self.klass = plan.klass
        
        super(FormType, self).__init__()
 
    @orm.reconstructor    
    def reconstruct(self):
        self.plan_identifier = self.plan.plan_identifier
        self.klass = self.plan.klass
        super(FormType, self).reconstruct()

    @property
    def __parent__(self):
        return LocationHelper(self.plan)
       
    @property 
    def __name__(self):
        return self.form_name

    def common_init(self):
        super(FormType, self).common_init()
        #self.__name__ =  self.form_name # Location awareness
        #self.__parent__ = LocationHelper(self.plan) # Location awareness
        self.operational = False
        if hasattr(self, 'klass'):
            self.op_setobject_type = setobject_type_registry.get(self.klass)
    
    def post_order_traverse(self, mode):
        super(FormType, self).post_order_traverse(mode)
            
        if hasattr(self, 'klass'):
            self.op_setobject_type = setobject_type_registry.get(self.klass)
            if self.op_setobject_type == None:
                raise Exception("Type '%s' does not exist. Check p2_plan " \
                    "table and/or ensure that class type exists in " \
                    "appropriate module and restart server." \
                    % (self.klass)
                )

    def widget_collection(self):
        for widget in self.widgets.itervalues():
            yield widget
  
    def make_operational(self, setobject):
        self.setobject = setobject
        self.op_setobject_id = setobject.id
        for (key, widget) in self.widgets.iteritems():
            widget.make_operational(setobject)
        self.operational = True
        return self
        
    def is_archetype(self):
        """ Check whether we are on an archetype form """
        return self.plan.is_archetype()
    
    #def set_attribute(self, attribute, value, mode):
    #    if attribute == 'css_style':
    #        selector = 'div[data-form-identifier="' + self.id + '"]'
    #        self.plan.update_css_rule(selector, value)
    #    else:
    #        SetobjectType.set_attribute(self, attribute, value, mode)
       
 
class FormTraverser(grok.Traverser):
    grok.context(FormType)

    def traverse(self, name):
        """Traversing over form to the widgets when a widget_identifier is given next."""
        return self.context.widgets[name]
