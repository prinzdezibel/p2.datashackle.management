# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import copy
import grok
import json

from grokcore.content import interfaces
from sqlalchemy import orm
from sqlalchemy.sql import and_, or_
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zope.location.interfaces import ILocation

from p2.datashackle.core import model_config
from p2.datashackle.core.app.setobjectreg import setobject_table_registry, setobject_type_registry
from p2.datashackle.core.models.setobject_types import SetobjectType
from p2.datashackle.core.models.identity import generate_random_identifier
from p2.datashackle.management.span.span import SpanFactory
from p2.datashackle.management.interfaces import IWidgetType
from p2.datashackle.management.span.span import Action, Label
from p2.datashackle.management.span.alphanumeric import Alphanumeric
from p2.datashackle.management.span.fileupload import Fileupload
from p2.datashackle.management.span.embeddedform import EmbeddedForm
from p2.datashackle.management.span.dropdown import Dropdown
from p2.datashackle.management.span.checkbox import Checkbox
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty
from p2.datashackle.core.interfaces import IDbUtility



@model_config()
class WidgetType(SetobjectType):
    grok.implements(IWidgetType, interfaces.IContext, ILocation)
    
    js_widget_constructor = 'p2.Widget'
    js_propertyform_constructor = 'p2.PropertyForm'
    
    def __init__(self):
        self.spans = dict()
        self.css = ''
        self.tab_order = 0
        self.widget_type = self.__class__.__name__.lower()
        super(WidgetType, self).__init__()

    @orm.reconstructor 
    def reconstruct(self):
        super(WidgetType, self).reconstruct()
        self.pre_order_traverse()

    def common_init(self):
        super(WidgetType, self).common_init()
        self.operational = False

    @property
    def __parent__(self):
        return self.form
       
    @property 
    def __name__(self):
        return self.id   

    def pre_order_traverse(self):
        if self.form == None:
            raise Exception("Can't finish initialization without the form attribute set.")
        
        # set op_setobject_type from parent form's attributes
        self.op_setobject_type = setobject_type_registry.lookup(self.form.klass)
        
        for span in self.spans.itervalues():
            span.widget = self
            span.op_setobject_type = self.op_setobject_type

    def make_operational(self, setobject):
        """Makes the widget operational, e.g. (potentially working on a user table via piggybacking spans)."""
        self.operational = True
        self.setobject = setobject
        self.op_setobject_id = setobject.id
        for (key, value) in self.spans.iteritems():
            self.spans[key].make_operational(setobject)
      
    def register_span(self, span_type, span_name):
        if not span_name in self.spans:
            self.spans[span_name] = span_type(span_name)
            self.spans[span_name].widget = self
        return self.spans[span_name]
        
    def lookup_view(self, request, view_mode, relation_linkage_id=None):
        # Check for specialized view class
        view = queryMultiAdapter((self, request), name=self.widget_type)
        if view == None:
            # Use the generalized class
            view = getMultiAdapter((self, request),
                                   name="widget")
            view.template_name = self.widget_type

        view.mode = view_mode         
   
        if relation_linkage_id is not None:
            view.relation_linkage_id = relation_linkage_id
        return view
    
    def is_archetype(self):
        """ Check whether we are on an archetype form """
        return self.form.is_archetype()
        
    @classmethod
    def map_computed_properties(cls):
        cls.sa_map_dispose()
        p2_widget = setobject_table_registry.lookup_by_class(WidgetType.__name__)    
        # Map base class
        orm.mapper(
            WidgetType,
            p2_widget,
            polymorphic_on=p2_widget.c.widget_type,
            polymorphic_identity='widgettype',
            properties=WidgetType.mapper_properties
            )
   
 
class PolymorphicWidget(WidgetType):

    @classmethod
    def map_computed_properties(cls):
        cls.sa_map_dispose()
        inherits = WidgetType._sa_class_manager.mapper
        orm.mapper(cls,
                 inherits=inherits,
                 polymorphic_identity=cls.__name__,
                 properties=cls.mapper_properties,
                 )



@model_config(maporder=2)
class ActionWidget(PolymorphicWidget):
     
    def __init__(self):
        super(ActionWidget, self).__init__()
        self.register_span(span_type=Action, span_name='button')


   
@model_config(maporder=2)
class CheckboxWidget(PolymorphicWidget):
 
    def __init__(self):
        super(CheckboxWidget, self).__init__()
        self.register_span(Label, 'label')
        self.register_span(Checkbox, 'piggyback')


@model_config(maporder=2)
class Labeltext(PolymorphicWidget):
    
    def __init__(self):
        super(Labeltext, self).__init__()
        self.register_span(Label, 'label')
        self.register_span(Alphanumeric, 'piggyback')

        
        
@model_config(maporder=2)
class FileuploadWidget(PolymorphicWidget):
    
    js_propertyform_constructor = 'p2.FileuploadPropertyform'
    js_widget_constructor = 'p2.Widget.Fileupload'
    
    def __init__(self):
        super(FileuploadWidget, self).__init__()
        self.register_span(Label, 'label')
        self.register_span(Fileupload, 'piggyback')
   

@model_config(maporder=2)
class EmbeddedFormWidget(PolymorphicWidget):

    js_propertyform_constructor = 'p2.RelationPropertyform'
    
    def __init__(self):
        super(EmbeddedFormWidget, self).__init__()
        self.register_span(Label, 'label')
        self.register_span(EmbeddedForm, 'piggyback')


@model_config(maporder=2) 
class DropdownWidget(PolymorphicWidget):
    
    js_propertyform_constructor = 'p2.DropdownPropertyform'
    
    def __init__(self):
        super(DropdownWidget, self).__init__()
        self.register_span(Label, 'label')
        self.register_span(Dropdown, 'piggyback')



class WidgetTraverser(grok.Traverser):
    grok.context(IWidgetType)

    def traverse(self, name):
        return self.context.spans[name]
        


class WidgetFactory(object):
    
    @classmethod
    def copy_widgets(cls, form_identifier):
        widgets = {}
        db_util = getUtility(IDbUtility)
        session = db_util.Session()
        query = session.query(WidgetType).filter_by(fk_p2_form=form_identifier)

        for widget in query:
            new = cls.create_widget(widget.widget_type)
            pk_keys = set([c.key for c in class_mapper(WidgetType).primary_key])
            cols = [p for p in class_mapper(WidgetType).iterate_properties 
                        if p.key not in pk_keys]
            for col in cols:
                if col.__class__ == ColumnProperty:
                    val = getattr(widget, col.key)
                    setattr(new, col.key, val)
                elif col.__class__ == RelationshipProperty:
                    if col.key == 'spans':
                        spans = SpanFactory.copy_spans(widget.id)
                        setattr(new, col.key, spans)
            widgets[new.id] = new
        return widgets

    
    @classmethod        
    def create_widget(cls, widget_type):
        widget_type = setobject_type_registry.lookup(widget_type)
        widget = widget_type()
        return widget

