# -*- coding: utf-8 -*-
import grok

from grokcore.layout import Page
from grokcore.layout.interfaces import IPage
from dolmen.forms.crud.interfaces import IFactoryAdding
from p2.datashackle.management.interfaces import IFormType
from p2.datashackle.management.form.views.base import LayoutAwareForm
from p2.datashackle.management.resource_library import (SetmanagerResources,
                                                        PlanResources,
                                                        AddModelResources)
from p2.datashackle.management.setobject_graph import SetobjectGraph
from p2.datashackle.management.content.generic_set import GenericSet
from p2.windowmanager.skin import WindowManagerSkin
from zope.publisher.interfaces.http import IHTTPRequest
from zeam.form.base import Actions, Action



class AddModelView(grok.MultiAdapter, LayoutAwareForm):

    class AddAction(Action):
        def __call__(self, form):
            graph_xml = form.request.form['data']
            graph = SetobjectGraph(form.request, graph_xml)
            graph.save()
            plan_id = form.request.form['plan_identifier']
            obj = GenericSet()
            obj.plan_identifier = str(plan_id)
            obj.title = plan_id
            obj.klass = str(form.request.form['klass'])
            obj.table_identifier = str(form.request.form['table_identifier'])
            form.adder.add(obj)
            return form.redirect(form.url(obj))
    
    actions = Actions(AddAction('add'),)
    grok.name('addmodelview')
    grok.adapts(IFormType, IHTTPRequest, IFactoryAdding)
    grok.provides(IPage)
    grok.context(IFormType)

    def __init__(self, context, request, adder):
        self.adder = adder
        LayoutAwareForm.__init__(self, context, request)

    def update(self):
        WindowManagerSkin.need()
        SetmanagerResources.need()
        PlanResources.need()
        AddModelResources.need()
        self.request.form['mode'] = 'OPERATIONAL'
        super(AddModelView, self).update()
    

