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
from p2.datashackle.management.interfaces import IFormType
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty
from p2.datashackle.management.widget.widget import WidgetFactory



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

    def __init__(self):

        # BEGIN sqlalchemy instrumented attributes
        # self.form_identifier initialized through SetobjectType base class.
        self.plan = None
        self.form_name = ''
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
    
       
 
class FormTraverser(grok.Traverser):
    grok.context(FormType)

    def traverse(self, name):
        return self.context.widgets[name]

        

class FormTypeFactory(object):
    
    @classmethod
    def copy(cls, plan_name, form_name):
        db_util = getUtility(IDbUtility)
        session = db_util.Session()
        form = session.query(FormType).filter_by(fk_p2_plan=plan_name, form_name=form_name).one()

        new = FormType()
        pk_keys = set([c.key for c in class_mapper(FormType).primary_key])
        cols = [p for p in class_mapper(FormType).iterate_properties 
                    if p.key not in pk_keys]
        for col in cols:
            if col.__class__ == ColumnProperty:
                val = getattr(form, col.key)
                setattr(new, col.key, val)
            elif col.__class__ == RelationshipProperty:
                if col.key == 'widgets':
                    widgets = WidgetFactory.copy_widgets(form.id)
                    setattr(new, col.key, widgets)
                else:
                    pass
                    #val = getattr(form, col.key)
                    #setattr(new, col.key, val)
        return new
