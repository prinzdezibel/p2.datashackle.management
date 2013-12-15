# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

from megrok import resource
#from p2.javascript.base import *
#from p2.windowmanager.layout import WindowManagerLibrary


class FormLibrary(resource.Library):
    resource.path('form/static')
form = resource.ResourceInclusion(FormLibrary, "form.js", depends=[])
propertyform = resource.ResourceInclusion(FormLibrary, "propertyform.js", depends=[])
dropdownpropertyform = resource.ResourceInclusion(FormLibrary, "dropdownpropertyform.js", depends=[])
relationpropertyform = resource.ResourceInclusion(FormLibrary, "relationpropertyform.js", depends=[])
fileuploadpropertyform = resource.ResourceInclusion(FormLibrary, "fileuploadpropertyform.js", depends=[])
changeableform = resource.ResourceInclusion(FormLibrary, "changeableform.js", depends=[])
designerform = resource.ResourceInclusion(FormLibrary, "designerform.js",
    depends=[])
objectpicker = resource.ResourceInclusion(FormLibrary, "objectpicker.js", depends=[])


class PlanResources(resource.ResourceLibrary):
    resource.path('model/static')
    resource.resource("designer.js", depends=[])
    resource.resource("datamanagement.js", depends=[])

class WidgetResources(resource.Library):
    resource.path('widget/static')
widget = resource.ResourceInclusion(WidgetResources, "widget.js", depends=[])
fileuploadwidget = resource.ResourceInclusion(WidgetResources, "fileupload.js", depends=[])
delete_dialog = resource.ResourceInclusion(WidgetResources, "delete_dialog.js", depends=[])
designer_formreset_dialog = resource.ResourceInclusion(WidgetResources, "designer_formreset_dialog.js", depends=[])


class SpanResources(resource.Library):
    resource.path('span/static')
span = resource.ResourceInclusion(SpanResources, "span.js", depends=[])
fileuploadspan = resource.ResourceInclusion(SpanResources, "fileupload.js", depends=[])
alphanumericspan = resource.ResourceInclusion(SpanResources, "alphanumeric.js", depends=[span])
actionspan = resource.ResourceInclusion(SpanResources, "action.js", depends=[span])
relationspan = resource.ResourceInclusion(SpanResources, "relation.js", depends=[span])
span_label = resource.ResourceInclusion(SpanResources, "label.js", depends=[span])
checkboxspan = resource.ResourceInclusion(SpanResources, "checkbox.js", depends=[span])
dropdownspan = resource.ResourceInclusion(SpanResources, "dropdown.js", depends=[span])


class SetmanagerLayoutResources(resource.ResourceLibrary):
    resource.path('static')
    resource.resource('setmanager_layout.js', depends=[])

class SetmanagerResources(resource.ResourceLibrary):
    resource.path('static')

    resource.resource('setobject.js', depends=[])
    resource.resource('setobject_graph.js', depends=[])
    resource.resource('setmanager.js',
                        depends=[form, designerform, changeableform,
                                 propertyform, relationpropertyform, fileuploadpropertyform,
                                 widget, fileuploadwidget,
                                 delete_dialog, designer_formreset_dialog,
                                 span, fileuploadspan, alphanumericspan, relationspan, span_label,
                                 actionspan, checkboxspan, objectpicker, dropdownspan, dropdownpropertyform,
                                 
                                 ]
                        )

class AddModelResources(resource.ResourceLibrary):
    resource.path('model/static')
    resource.resource("addmodel.js", depends=[])
