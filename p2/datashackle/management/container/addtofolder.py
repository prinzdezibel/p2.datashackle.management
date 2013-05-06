# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.de, 2011
# Author: Michael Jenny

import grok
import dolmen.app.container
from dolmen.app.container.listing import FolderListing
from dolmen.app.layout import IDisplayView, AboveBody
from dolmen.content.interfaces import IContainer

#import dolmen.app.container
#import grokcore.viewlet as grok
#
#from dolmen.app import security, layout
from p2.datashackle.management.interfaces import IFolder
from p2.datashackle.management.interfaces import IDatashackleContentFactory
from zope.component import getUtilitiesFor, queryMultiAdapter
#from zope.container.constraints import checkFactory
#from zope.security.checker import CheckerPublic
#from zope.security.management import checkPermission



class AddMenu(dolmen.app.container.AddMenu):
    grok.view(FolderListing)
    grok.context(IFolder)

    def update(self):
        """Gathers the factories allowed for the context container
        in a list of factories information useable by the template.
        """
        self.factories = []
        self.contexturl = self.view.url(self.context)


        for name, factory in getUtilitiesFor(IDatashackleContentFactory):
            # We iterate and check the factories
            if self.checkFactory(name, factory):
                factory_class = factory.factory
                icon_view = queryMultiAdapter(
                    (factory_class, self.request), name="icon")
                self.factories.append(dict(
                    name=name,
                    icon=(icon_view() if icon_view else None),
                    id=name.replace(".", "-"),
                    url='%s/++%s++%s' % (self.contexturl,
                                         factory.addtraversal,
                                         name),
                    title=factory_class.__content_type__,
                    description=(factory.description or
                                 factory_class.__doc__),
                    ))



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
    

