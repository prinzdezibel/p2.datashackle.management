# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
from zope.interface import Interface
from megrok import resource
from dolmen.app.layout.master import Header
from skin import ISetmanagerLayer

from js.jquery import jquery

from p2.datashackle.management.resource_library import FormLibrary, \
    SetmanagerLayoutResources    
from p2.datashackle.management import xmlDOM, jqueryui, p2_js, cookies_js, \
    multiple_inheritance_js, window_js, windowmanager_js


class SetmanagerLibrary(resource.ResourceLibrary):
    grok.name("setmanager.ui.skin")
    grok.layer(ISetmanagerLayer)
    resource.path('static')
    resource.resource('setmanager.css')
    resource.resource('dropdown.js', depends=[])


class SetmanagerResourceViewlet(grok.Viewlet):
    grok.viewletmanager(Header)
    grok.layer(ISetmanagerLayer)
    grok.context(Interface)
    
    def update(self):
        multiple_inheritance_js.need()
        p2_js.need()
        cookies_js.need()
        jquery.need()
        jqueryui.need()
        window_js.need()
        windowmanager_js.need()
        SetmanagerLibrary.need()
        xmlDOM.need()
        SetmanagerLayoutResources.need()
 
    def render(self):
        return u""
    
