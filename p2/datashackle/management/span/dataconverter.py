# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2011
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
from zope.interface import Interface
from p2.datashackle.core import ModelBase
from p2.datashackle.core.app.exceptions import SetobjectGraphException


class IDataConverter(Interface):
    def to_span_value(value):
        """Converts the value of a database mapped setobject attribute to a format
        suitable to be displayed within a HTML document.
        """
    def to_field_value(value):
        """Converts the value from the HTML form into a format that can be assigned
        to a mapped setobject attribute.
        """


class DataConverter(grok.Adapter):
    """A base implementation of the data converter."""
    grok.implements(IDataConverter)
    grok.provides(IDataConverter)
    #grok.adapts(ModelBase, IHTTPRequest)
    grok.context(ModelBase)

    def to_span_value(value):
        return value

    def to_field_value(value):
        return value


