# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
from dolmen.app import layout
from zope.interface import Interface
from zope.publisher.interfaces import browser


class ISetmanagerLayer(layout.IBaseLayer):
    """marker interface"""


class ISetmanagerSkin(ISetmanagerLayer, browser.IBrowserSkinType):
    """A skin for the setmanager site."""
    grok.skin("setmanager")
    
