# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok,grokcore
from grok import IApplication

from dolmen.menu import menuentry
from dolmen.app.layout import Page
from dolmen.app.layout import ContextualMenu
from zope.component import getUtility, getMultiAdapter
from sqlalchemy.sql import not_ 

from p2.javascript.base import *
from p2.datashackle.management import MF as _
from p2.datashackle.management.interfaces import IGenericSet
from p2.datashackle.core.interfaces import IFormType
from p2.datashackle.management.resource_library import SetmanagerResources, PlanResources
from p2.windowmanager.layout import WindowManagerLibrary
from p2.windowmanager.skin import WindowManagerSkin
from p2.datashackle.core.app.setobjectreg import setobject_table_registry, setobject_type_registry

    
@menuentry(ContextualMenu, order=20)  
class DesignerView(Page):
    grok.context(IGenericSet)
    grok.name('designerview')
    grok.title(_(u"Designer"))
    grok.require("dolmen.content.Edit")
    
    @property
    def parent_application(self):
        """ Traverse 'backwards' to find the application object again """
        node = self.context
        while node is not None:
            if IApplication.providedBy(node): return node
            node = getattr(node, '__parent__', None)
        return None

    def update(self):
        super(DesignerView, self).update()
        
        # Needed libraries for view
        WindowManagerLibrary.need()
        WindowManagerSkin.need()
        SetmanagerResources.need()
        PlanResources.need()
        binpack.need()
            
    def render(self):
        template = grokcore.view.PageTemplateFile("templates/designerview.pt")
        html = template.render(self)
        return html


    def lookup_archetype_view(self):
        app = grok.getApplication()
        archetype_genericset = app['configuration']['meta']['p2_archetypes']
        plan = archetype_genericset.plan
        form = plan.forms['archetypes']
        view = getMultiAdapter(
            (form, self.request),
            context=IFormType,
            name='baseform'
            )
        # ATTENTION: Displaying the archetype form does not mean it is in archetype mode.
        # That mode is for ajax requests when dropping widget into designer form.
        self.request.form['mode'] = 'DESIGNER'
        return view()
            
    def forms_for_plan(self):
        for form_name, form in self.context.plan.forms.iteritems():
            yield form
