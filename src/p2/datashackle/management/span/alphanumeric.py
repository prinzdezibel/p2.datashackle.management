# -*- coding: utf-8 -*-
# Copyright(C) projekt-und-partner.com, 2011
# Author: Michael Jenny

import datetime
import grok

from sqlalchemy import orm
from sqlalchemy import String
from zope.component import getUtility, queryAdapter
from zope.i18n.format import DateTimeParseError
from zope.publisher.interfaces import IRequest
from zope.security.interfaces import NoInteraction
from zope.security.management import getInteraction

from p2.datashackle.core import model_config
from p2.datashackle.core.app.exceptions import SetobjectGraphException
from p2.datashackle.core.app.setobjectreg import setobject_table_registry, \
    setobject_type_registry
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.core.models.mapping import map_field_attr
from p2.datashackle.core.models.setobject_types import SetobjectType
from p2.datashackle.management.span.dataconverter import IDataConverter, DataConverter
from p2.datashackle.management.span.span import SpanType


@model_config(tablename='p2_span_alphanumeric', maporder=3)
class Alphanumeric(SpanType):
 
    def __init__(self, span_name=None):
        self.required = True
        ft = setobject_type_registry.lookup('p2.datashackle.core.models.setobject_types', 'p2_fieldtype')
        sess = getUtility(IDbUtility).Session()
        self.field_type = sess.query(ft).filter_by(field_type='textline').one()
        self.css_style = "left:" + str(self.label_width) + "px; width:" + str(self.label_width) + "px;"
        super(Alphanumeric, self).__init__(span_name)

    def _get_info(self):
        info = {}
        if self.operational:
            piggyback = self.piggyback
            converter = queryAdapter(self, name=self.field_type.field_type, interface=IDataConverter)
            if converter is not None:
                piggyback = converter.to_span_value(piggyback) 
            info['piggyback'] = piggyback
            info['attr_name'] = self.attr_name
        info['field_type'] = str(self.field_type.field_type).lower()
        info['required'] = self.required
        return info
    
    def make_operational(self, setobject):
        super(Alphanumeric, self).make_operational(setobject)
        if getattr(setobject, self.attr_name) == None:
            self.piggyback = self.span_value
        else:
            self.piggyback = getattr(setobject, self.attr_name)

    @classmethod
    def map_computed_properties(cls):
        cls.sa_map_dispose()
        alphanumeric_table = setobject_table_registry.lookup_by_class(cls.__module__, cls.__name__)
        inherits = SpanType._sa_class_manager.mapper
        orm.mapper(Alphanumeric,
                   alphanumeric_table,
                   inherits=inherits,
                   properties = cls.mapper_properties,
                   polymorphic_identity='alphanumeric')
   
    def onbefore_set_payload_attribute(self, setobject, attribute, value, mode):
        # Parameter `value` can be a native type (string, boolean) or another setobject
        if mode == 'save':
            converter = queryAdapter(self, name=self.field_type.field_type, interface=IDataConverter)
            if converter != None:
                value = converter.to_field_value(value)
            if self.required == True and (value == None or len(value) == 0):
                raise SetobjectGraphException("Missing field '%s' required." % (attribute), setobject.id)
            return value
 
    def post_order_traverse(self, mode):
        if mode == 'save':
            so_type = setobject_type_registry.lookup(
                self.op_setobject_type.__module__,
                self.op_setobject_type.__name__)
            table_name = so_type.get_table_name()
            map_field_attr(
                table_name,
                self.field_identifier,
                String(255))


class DateConverter(DataConverter):
    grok.name('date')
    
    def __init__(self, context):
        super(DateConverter, self).__init__(context)
        request = self.get_request()
        self.formatter = request.locale.dates.getFormatter('date', None)

    def to_span_value(self, value):
        if value is None:
            return
        # parse from string with datetime's strptime function.
        # In the end we are only interested in datetime's date() part (no time).
        try:
            dt = datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            # Formatting error. The corrupt value will be displayed anyway.
            return value
        return self.formatter.format(dt.date())

    def to_field_value(self, value):
        if value is None:
            return
        try:
            date = self.formatter.parse(value)
            # Dates are saved in ISO 8601 format into database.
            return date.isoformat()
        except DateTimeParseError, err:
            msg = err.args[0]
            raise SetobjectGraphException(msg, self.context.id)
           
    def get_request(self):
        try:
            i = getInteraction() # raises NoInteraction
        except NoInteraction:
            raise Exception("No request error.")
    
        for p in i.participations:
            if IRequest.providedBy(p):
                return p
        raise Exception("No request error.")
     
