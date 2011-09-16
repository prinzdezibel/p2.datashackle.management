# -*- coding utf-8 -*-
# Copyright (C) projekt-und-partner.de, 2011
# Author: Michael Jenny

import grok

import dolmen.content

from dolmen import menu
from dolmen.app.content import icon
from dolmen.app.layout import ContextualMenu
from menhir.contenttype.privatefolder import PrivateFolder

from p2.container.listing import FolderListing
from p2.datashackle.core import MF as _
from p2.datashackle.core.app.properties import TranslatableDescriptiveProperties
from p2.datashackle.core.interfaces import IFolder, IListingDefault



class PrivateFolder(TranslatableDescriptiveProperties, PrivateFolder):
    grok.implements(IListingDefault)
    dolmen.content.nofactory()


@menu.menuentry(ContextualMenu, order=40)
class FolderListing(FolderListing):
     """The folderlisting view should be available as index view.
     """
     grok.context(IListingDefault)
     grok.name('index')


    

class Folder(TranslatableDescriptiveProperties, dolmen.content.OrderedContainer):
    icon('folder.png')
    grok.implements(IFolder)
    dolmen.content.schema(IFolder)
    dolmen.content.name(_(u"Folder"))
    
    

 

