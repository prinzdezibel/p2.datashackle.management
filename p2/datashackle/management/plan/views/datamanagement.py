# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
import json
from dolmen.forms import base as form
from dolmen.app.layout import Index
from dolmen.app.layout import ContextualMenu
from dolmen.menu import menuentry
from zope.interface import Interface, implements

from p2.datashackle.management import MF as _
from p2.datashackle.management.resource_library import SetmanagerResources, PlanResources 
from p2.datashackle.management.setobject_graph import SetobjectGraph
from p2.datashackle.management.interfaces import IGenericSet
from p2.datashackle.core.app.exceptions import SetobjectGraphException
from p2.windowmanager.skin import WindowManagerSkin

from zeam.form.layout.form import Form
from zeam.form.base import Actions, Action
from grokcore.layout.interfaces import ILayout, IPage


@menuentry(ContextualMenu, order=10)    
class EditData(Form):
    class SaveAction(Action):
        def __call__(self, form):
            form.saved = True
            jsonresponse = dict()

            graph_xml = form.request.form['data']

            try:
                graph = SetobjectGraph(form.request, graph_xml)
                graph.save()
                jsonresponse['result'] = 'OK'
            except SetobjectGraphException, ex:
                jsonresponse['error'] = {'title': 'Save failed',
                                          'message': ex.reason,
                                          'data_node_id': ex.setobjectid}
            form.jsonresponse = jsonresponse

    
    grok.name('index') 
    grok.context(IGenericSet)
    grok.title(_(u"Edit data"))
    grok.require('dolmen.content.View')

    actions = Actions(SaveAction('Save'),)
    saved = False

    @property
    def prefix(self):
        return str(self.context.plan_identifier)
        
    def update(self):

        self.context_url = grok.url(self.request, self.context)
        super(EditData, self).update()
         
        # Needed libraries for view
        WindowManagerSkin.need()
        PlanResources.need()
        SetmanagerResources.need()

    def render(self):
        if self.context.plan_identifier == "p2_meta_property_form" or self.context.plan_identifier == "p2_meta_archetype":
            return ""

        if self.saved:
            self.response.setHeader('Content-Type', 'application/json')
            return json.dumps(self.jsonresponse)
        else: 
            template = grok.PageTemplateFile("../templates/datamanagementview.pt")
            html = template.render(self)
            return html


