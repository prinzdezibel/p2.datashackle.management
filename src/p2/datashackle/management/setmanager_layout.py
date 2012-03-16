# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
from zope.interface import Interface
from megrok import resource
from megrok.layout import Layout

from p2.datashackle.management.skin import ISetmanagerLayer 
    

class SetmanagerLayout(Layout):
    grok.context(Interface)
    grok.layer(ISetmanagerLayer)
    template = grok.PageTemplateFile('setmanager_layout.pt')

    def update(self):
        self.base = self.request.getApplicationURL()
