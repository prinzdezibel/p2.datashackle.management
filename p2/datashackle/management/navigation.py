# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok

from zope.interface import Interface
from menhir.simple.navtree import NavTree
from dolmen.app.layout import Top

from p2.datashackle.management.skin import ISetmanagerLayer

class NavigationVM(grok.ViewletManager):
    grok.name('setmanager.navigation')
    grok.context(Interface)
    
# we don't want the original viewlet to be rendered
class BlanketNavTree(grok.Viewlet):
    grok.name('navtree')
    grok.context(Interface)
    grok.layer(ISetmanagerLayer)
    grok.viewletmanager(Top)
    
    def render(self):
        return u""
    
class Navigation(NavTree):
    grok.context(Interface)
    grok.viewletmanager(NavigationVM)
