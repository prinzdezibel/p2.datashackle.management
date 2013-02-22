# -*- coding: utf-8 -*-
import grok

from grokcore.layout import Page
from grokcore.layout.interfaces import IPage
from dolmen.forms.crud.interfaces import IFactoryAdding
from p2.datashackle.management.interfaces import IFormType
from p2.datashackle.management.form.views.base import BaseForm
from p2.datashackle.management.resource_library import SetmanagerResources, PlanResources
from p2.datashackle.management.setobject_graph import SetobjectGraph
from p2.datashackle.management.content.generic_set import GenericSet
from p2.windowmanager.skin import WindowManagerSkin
from zope.publisher.interfaces.http import IHTTPRequest


class AddModelView(grok.MultiAdapter, Page, BaseForm):
    grok.name('addmodelview')
    grok.adapts(IFormType, IHTTPRequest, IFactoryAdding)
    grok.provides(IPage)

    def __init__(self, context, request, adder):
        self.adder = adder
        BaseForm.__init__(self, context, request)

    def update(self):
        if 'action' in self.request.form and self.request.form['action'] == 'add':
            graph_xml = self.request.form['data']
            graph = SetobjectGraph(self.request, graph_xml)
            graph.save()
            plan_id = self.request.form['plan_identifier']
            obj = GenericSet()
            obj.plan_identifier = str(plan_id)
            obj.title = plan_id
            obj.table_identifier = str(self.request.form['table_identifier'])
            self.adder.add(obj)
            return self.redirect(self.url(obj))

            
        WindowManagerSkin.need()
        SetmanagerResources.need()
        PlanResources.need()
        self.request.form['mode'] = 'OPERATIONAL'
        super(AddModelView, self).update()
    


