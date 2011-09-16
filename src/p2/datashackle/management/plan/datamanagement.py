# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok,grokcore

from dolmen.forms import base as form
from dolmen.app.layout import Index
from dolmen.app.layout import ContextualMenu
from dolmen.menu import menuentry
from zope.interface import Interface, implements

from p2.datashackle.core import MF as _
from p2.datashackle.management.resource_library import SetmanagerResources, PlanResources 
from p2.datashackle.core.interfaces import IPlan, IGenericSet
from p2.windowmanager.layout import WindowManagerLibrary
from p2.windowmanager.skin import WindowManagerSkin


@menuentry(ContextualMenu, order=10)    
class EditData(Index):
    grok.context(IGenericSet)
    grok.title(_(u"Edit data"))
    grok.require('dolmen.content.View')
        
    def update(self):

        self.context_url = grok.url(self.request, self.context)
        super(EditData, self).update()
        self.new_setobject = "%s/newobjectview" % (
                                         grok.url(self.request, self.context))
        SetmanagerResources.need()
        
        # Needed libraries for view
        WindowManagerLibrary.need()
        WindowManagerSkin.need()
        PlanResources.need()


    def render(self):
        if self.context.plan_identifier == "p2_meta_property_form" or self.context.plan_identifier == "p2_meta_archetype":
            return ""
        template = grokcore.view.PageTemplateFile("templates/datamanagementview.pt")
        html = template.render(self)
        return html
