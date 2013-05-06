# -*- coding: utf-8 -*-
# Copyright(C) projekt-und-partner.com, 2011
# Author: Michael Jenny

from sqlalchemy import orm
from sqlalchemy import Boolean

from p2.datashackle.core import model_config
from p2.datashackle.core.models.mapping import map_field_attr
from p2.datashackle.core.models.setobject_types import setobject_table_registry, \
    setobject_type_registry
from p2.datashackle.management.span.span import PolymorphicSpanType


@model_config(maporder=3)
class Checkbox(PolymorphicSpanType):


    def __init__(self, span_name=None):
        self.css = "left:" + str(self.label_width) + "px;"
        super(Checkbox, self).__init__(span_name)

    def _get_info(self):
        info = {}
        if self.operational:
            info['piggyback'] = self.piggyback
            info['attr_name'] = self.attr_name
        return info
    
    def post_order_traverse(self, mode):
        if mode == 'save':
            so_type = setobject_type_registry.lookup(self.op_setobject_type.__name__)
            table_name = so_type.get_table_name()
            map_field_attr(
                table_name,
                self.field_identifier,
                Boolean)
 
    def make_operational(self, setobject):
        super(Checkbox, self).make_operational(setobject)
        if getattr(setobject, self.attr_name) == None:
            self.piggyback = self.span_value
        else:
            self.piggyback = getattr(setobject, self.attr_name)


        
