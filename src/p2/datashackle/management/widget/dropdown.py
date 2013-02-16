# -*- coding: utf-8 -*-
# Copyright(C) projekt-und-partner.com, 2011
# Author: Michael Jenny

import grok

from sqlalchemy import orm

from p2.datashackle.core import model_config
from p2.datashackle.management.interfaces import IWidgetType
from p2.datashackle.management.widget.widget import WidgetType


@model_config(maporder=2) 
class DropdownWidget(WidgetType):
    grok.implements(IWidgetType)
    
    js_propertyform_constructor = 'p2.DropdownPropertyform'
    
    def __init__(self):
        super(Dropdown, self).__init__()
        self.register_span('label', 'label')
        self.register_span('dropdown', 'piggyback')

    @classmethod
    def map_computed_properties(cls):
        cls.sa_map_dispose()
        inherits = WidgetType._sa_class_manager.mapper
        orm.mapper(DropdownWidget,
            inherits=inherits,
            properties=DropdownWidget.mapper_properties,
            polymorphic_identity='dropdown')

