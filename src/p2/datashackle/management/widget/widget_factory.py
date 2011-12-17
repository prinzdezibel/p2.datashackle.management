# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

from zope.component import getUtility

from p2.datashackle.management.widget.dropdown import Dropdown
from p2.datashackle.management.widget.widget import Labeltext, \
    Checkbox, Action, Fileupload, EmbeddedForm

def lookup_widget_type(widgettype):
    widgettype = str(widgettype).lower()
    if widgettype == 'labeltext':
        return Labeltext
    elif widgettype == 'checkbox':
        return Checkbox
    elif widgettype == 'embeddedform':
        return EmbeddedForm
    elif widgettype == 'action':
        return Action
    elif widgettype == 'relation':
        return Relation
    elif widgettype == 'fileupload':
        return Fileupload
    elif widgettype == 'dropdown':
        return Dropdown
    else:
        raise UnspecificException("Unknown widgettype.")

        
def create_widget(widget_type):
    widget_type = lookup_widget_type(widget_type)
    widget = widget_type()
    return widget
