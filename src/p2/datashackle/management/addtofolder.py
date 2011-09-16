# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.de, 2011
# Author: Michael Jenny

import grok

from dolmen.app.container.addtofolder import AddMenu
from dolmen.app.container.listing import FolderListing
from dolmen.app.layout import IDisplayView, AboveBody
from dolmen.content.interfaces import IContainer


class AddMenu(AddMenu):
    """Normally the Add-to-folder" menu viewlet is rendered on the DefaultView (index).
    This is not wanted here. We want to appear it on the FolderListing.
    """
    grok.order(60)
    grok.view(FolderListing)


class HideAddMenu(grok.Viewlet):
    """Normally the Add-to-folder" menu viewlet is rendered on the DefaultView (index).
    This is not wanted here. Therefore we discriminate the view against our own context and
    render an empty string.
    """
    grok.name('addmenu')
    grok.context(IContainer)
    grok.view(IDisplayView)
    grok.viewletmanager(AboveBody)
    
    def render(self):
        return u''
    

