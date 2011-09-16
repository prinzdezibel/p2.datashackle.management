# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

from hurry.jquery import jquery
from megrok import resource
from p2.javascript.base import *
from p2.windowmanager.layout import WindowManagerLibrary


class FormLibrary(resource.Library):
    resource.path('form/static')
form = resource.ResourceInclusion(FormLibrary, "form.js", depends=[jquery, jBase])

propertyform = resource.ResourceInclusion(FormLibrary, "propertyform.js", depends=[jquery, jBase])
dropdownpropertyform = resource.ResourceInclusion(FormLibrary, "dropdownpropertyform.js", depends=[jquery, jBase])
relationpropertyform = resource.ResourceInclusion(FormLibrary, "relationpropertyform.js", depends=[jquery, jBase])
fileuploadpropertyform = resource.ResourceInclusion(FormLibrary, "fileuploadpropertyform.js", depends=[jquery, jBase])
changeableform = resource.ResourceInclusion(FormLibrary, "changeableform.js", depends=[jquery, jBase])
designerform = resource.ResourceInclusion(FormLibrary, "designerform.js", depends=[jquery, form, jBase, WindowManagerLibrary])
objectpicker = resource.ResourceInclusion(FormLibrary, "objectpicker.js", depends=[jquery])

class PlanResources(resource.ResourceLibrary):
    resource.path('plan/static')
    resource.resource("designer.js", depends=[jquery, jBase])
    resource.resource("datamanagement.js", depends=[jquery, jBase])

class WidgetResources(resource.Library):
    resource.path('widget/static')
widget = resource.ResourceInclusion(WidgetResources, "widget.js", depends=[jquery, jBase])
fileuploadwidget = resource.ResourceInclusion(WidgetResources, "fileupload.js", depends=[jquery, jBase])
delete_dialog = resource.ResourceInclusion(WidgetResources, "delete_dialog.js", depends=[jqueryui, jBase])
designer_formreset_dialog = resource.ResourceInclusion(WidgetResources, "designer_formreset_dialog.js", depends=[jqueryui, jBase])


class SpanResources(resource.Library):
    resource.path('span/static')
span = resource.ResourceInclusion(SpanResources, "span.js", depends=[jquery, jBase])
fileuploadspan = resource.ResourceInclusion(SpanResources, "fileupload.js", depends=[html5_upload, span])
alphanumericspan = resource.ResourceInclusion(SpanResources, "alphanumeric.js", depends=[span])
actionspan = resource.ResourceInclusion(SpanResources, "action.js", depends=[span])
relationspan = resource.ResourceInclusion(SpanResources, "relation.js", depends=[span])
span_label = resource.ResourceInclusion(SpanResources, "label.js", depends=[span])
checkboxspan = resource.ResourceInclusion(SpanResources, "checkbox.js", depends=[span])
dropdownspan = resource.ResourceInclusion(SpanResources, "dropdown.js", depends=[span])


class SetmanagerLayoutResources(resource.ResourceLibrary):
    resource.path('static')
    resource.resource('setmanager_layout.js', depends=[jBase, jquery, jqueryui])

class SetmanagerResources(resource.ResourceLibrary):
    resource.path('static')

    resource.resource('setobject.js', depends=[jBase])
    resource.resource('setobject_graph.js', depends=[jBase])
    resource.resource('setmanager.js',
                        depends=[jquery, jqueryui, jquerytools, jBase,
                                 form, designerform, changeableform,
                                 propertyform, relationpropertyform, fileuploadpropertyform,
                                 widget, fileuploadwidget,
                                 xmlDOM, delete_dialog, designer_formreset_dialog,
                                 span, fileuploadspan, alphanumericspan, relationspan, span_label,
                                 actionspan, checkboxspan, objectpicker, dropdownspan, dropdownpropertyform
                                 ]
                        )
