# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
from zope.interface import Interface

from p2.datashackle.management.interfaces import IGenericSet
from p2.windowmanager.layout import WindowManager


class WindowManagerVM(grok.ViewletManager):
    grok.name("windowmanager")
    grok.context(Interface)


class WindowManager(WindowManager):
    grok.context(IGenericSet)
    grok.viewletmanager(WindowManagerVM)
    grok.order(20)
