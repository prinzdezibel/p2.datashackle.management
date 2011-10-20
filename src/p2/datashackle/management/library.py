# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
from zope.interface import Interface
from hurry.jquery import jquery
from megrok import resource
from dolmen.app.layout.master import Header
from p2.javascript.base import *
from skin import ISetmanagerLayer

class SetmanagerLibrary(resource.ResourceLibrary):
    grok.name("setmanager.ui.skin")
    grok.layer(ISetmanagerLayer)
    resource.path('static')
    resource.resource('setmanager.css')
    resource.resource('dropdown.js', depends=[jquery])


class SetmanagerResourceViewlet(grok.Viewlet):
    grok.viewletmanager(Header)
    grok.layer(ISetmanagerLayer)
    grok.context(Interface)
    
    def render(self):
        SetmanagerLibrary.need()
        return u""
    
