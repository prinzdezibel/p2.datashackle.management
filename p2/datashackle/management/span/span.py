# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import copy
import grok
import json
import random

from sqlalchemy import orm
from zope.component import getMultiAdapter, queryMultiAdapter, getUtility
from zope.app.appsetup.interfaces import IDatabaseOpenedWithRootEvent
from zope.catalog.interfaces import ICatalog
from zope.location.interfaces import ILocation

from p2.datashackle.core import model_config
from p2.datashackle.core.app.exceptions import *
from p2.datashackle.core.app.setobjectreg import (setobject_table_registry,
                                                  setobject_type_registry)
from p2.datashackle.core.models.setobject_types import SetobjectType
from p2.datashackle.management.interfaces import ISpanType
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty



@model_config()
class SpanType(SetobjectType):
    grok.implements(ISpanType, ILocation)
    
    label_width = 95
    operational = False # Designer mode or user mode?
    action = None
 
    def __init__(self, span_name=None):
        super(SpanType, self).__init__()
        self.widget = None
        self.span_name = span_name
        self.span_type = self.__class__.__name__.lower()
        self.visible = True
        self.css = ''
     
    def common_init(self):
        super(SpanType, self).common_init()
        self.op_setobject_id = None
        self.op_setobject_type = None
    
    @orm.reconstructor 
    def reconstruct(self):
        super(SpanType, self).reconstruct()
        
    def make_operational(self, setobject):
        self.operational = True
        self.setobject = setobject
        self.op_setobject_id = setobject.id
    
    @property
    def __parent__(self):
        return self.widget
       
    @property 
    def __name__(self):
        return self.span_name   
 
    def onbefore_set_payload_attribute(self, setobject, attribute, value, mode):
        """This method is called when an attribute of this span's payload (a user setobject
        or a native object attribute like a string) is going to be set.
        """
        return value

    def onbefore_post_order_traverse(self, setobject, mode):
        """Called before a span's setobject is travered in post order.
        """    
 
    def lookup_view(self, request, view_mode, relation_linkage_id=None):
        # Check for specialized view class
        view = queryMultiAdapter((self, request), name=self.span_type)
        if view == None:
            # Use the generalized class
            view = getMultiAdapter((self, request), context=self, name='SpanType')
        view.template_name = self.span_type
        view.mode = view_mode

        if relation_linkage_id is not None:
            view.relation_linkage_id = relation_linkage_id

        return view
    
    def _get_info(self):
        """This method is intended to be overwritten by subclasses."""
        return {}
    
    def get_info(self):
        info = {'operational': self.operational,
                'module': self.operational and self.op_setobject_type and self.op_setobject_type.__module__ or self.__class__.__module__,
                'type': self.operational and self.op_setobject_type and self.op_setobject_type.__name__ or self.__class__.__name__,
                'data_node_id': self.operational and self.op_setobject_id or self.span_identifier,
                'css': self.css,
                'span_type': self.span_type,
                'span_name': self.span_name,
                'action': self.operational and self.setobject.action or self.action,
                'span_value': self.span_value,
                'visible': self.visible,
                'span_identifier': self.span_identifier,
                'archetype': self.is_archetype(),
                }
                
        if not self.operational:
            info['attr_name'] = 'span_value'
                
        # Extend the above with type specific info.
        info.update(self._get_info())
        json_info = json.dumps(info)
        return json_info
        
    def is_archetype(self):
        """ Check whether we are on an archetype form """
        return self.widget.is_archetype()
             
    @classmethod
    def map_computed_properties(cls):
        cls.sa_map_dispose()
        table_type = setobject_table_registry.lookup_by_class(SpanType.__name__)

        # Map base class
        #    
        # with_polymorphic="*":  This loads attributes from tables that use
        # joined table inheritance (p2_span_embeddedform) as well.
        # when doing something like query(SpanType).filter(RelationSpan.span_identifier = relation_span_id)
        span_mapper = orm.mapper(
            cls,
            table_type,
            polymorphic_on=table_type.c.span_type,
            polymorphic_identity='spantype',
            properties=cls.mapper_properties,
            with_polymorphic='*'
       )
    
  
from p2.datashackle.core.interfaces import IDbUtility

class PolymorphicSpanType(SpanType):
    @classmethod
    def map_computed_properties(cls):
        from p2.datashackle.management.plan.plan import Plan 
        t = setobject_table_registry.lookup_by_class(Plan.__name__)
        select = t.select().where(t.c.klass == cls.__name__)
        rec = dict(select.execute().first())
        
        cls.sa_map_dispose()
        if rec['table'] == SpanType.get_table_name():
            orm.mapper(cls,
                       inherits=SpanType._sa_class_manager.mapper,
                       polymorphic_identity=cls.__name__,
                       properties=cls.mapper_properties)
        else:
            table = setobject_table_registry.lookup_by_class(cls.__name__)
            orm.mapper(cls,
                       table,
                       inherits=SpanType._sa_class_manager.mapper,
                       polymorphic_identity=cls.__name__,
                       properties=cls.mapper_properties)


@model_config(maporder=3)
class Label(PolymorphicSpanType):

    def __init__(self, span_name=None):
        self.field_type = 'text'
        self.css = "width:" + str(self.label_width) + "px;"
        super(Label, self).__init__(span_name)

 
@model_config(maporder=2) 
class Action(PolymorphicSpanType):

    def _get_info(self):
        info = {}
        info['aktion'] = self.aktion
        return info


class SpanFactory(object):

       
    @classmethod
    def copy_spans(cls, widget_id):
        spans = {}

        db_util = getUtility(IDbUtility)
        session = db_util.Session()
        query = session.query(SpanType).filter_by(fk_p2_widget=widget_id)

        for span in query:
            new = cls.create_span(span.span_type, span.span_name)
            pk_keys = set([c.key for c in class_mapper(new.__class__).primary_key])
            cols = [p for p in class_mapper(new.__class__).iterate_properties 
                        if p.key not in pk_keys]
            for col in cols:
                if col.__class__ == ColumnProperty:
                    if col.key == 'order':
                        continue # order field is autoincremented
                    val = getattr(span, col.key)
                    setattr(new, col.key, val)
            spans[span.span_name] = new
        return spans

    @classmethod
    def create_span(cls, span_type_name, span_name):
        span_type = setobject_type_registry.lookup(span_type_name)
        return span_type(span_name)

