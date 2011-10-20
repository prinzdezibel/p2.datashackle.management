# -*- coding: utf-8 -*-
# Copyright(C) projekt-und-partner.com, 2011
# Author: Michael Jenny

from sqlalchemy import orm

from p2.datashackle.core import model_config
from p2.datashackle.management.span.span import SpanType

@model_config(tablename='p2_span', maporder=3)
class Label(SpanType):

    @classmethod
    def map_computed_properties(cls):
        cls.sa_map_dispose()
        inherits = SpanType._sa_class_manager.mapper
        orm.mapper(Label,
                    inherits=inherits,
                    polymorphic_identity='label',
                    properties=cls.mapper_properties,
                  )
    
    def __init__(self, span_name=None, objid=None):
        self.field_type = 'text'
        self.css_style = "width:" + str(self.label_width) + "px;"
        super(Label, self).__init__(span_name, objid)

