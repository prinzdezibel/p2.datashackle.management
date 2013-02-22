# -*- coding utf-8 -*-
# Copyright (C) projekt-und-partner.de, 2011
# Author: Michael Jenny

import grok

import dolmen.content

from dolmen import menu
from dolmen.app.content import icon
from dolmen.app.layout import ContextualMenu

from p2.container.listing import FolderListing
from p2.datashackle.management.properties import TranslatableDescriptiveProperties
from p2.datashackle.management.interfaces import IFolder, IListingDefault
from p2.datashackle.management.interfaces import IDatashackleContentFactory
from p2.datashackle.management.content.factoring import DatashackleContentFactory




@menu.menuentry(ContextualMenu, order=40)
class FolderListing(FolderListing):
     """The folderlisting view should be available as index view.
     """
     grok.context(IListingDefault)
     grok.name('index')
    
class FolderFactory(DatashackleContentFactory):
    dolmen.content.name('Folder')

class Folder(TranslatableDescriptiveProperties, dolmen.content.OrderedContainer):
    icon('folder.png')
    grok.implements(IFolder)
    dolmen.content.schema(IFolder)
    dolmen.content.name(u"Folder")
    dolmen.content.factory(FolderFactory)
    
    

 

