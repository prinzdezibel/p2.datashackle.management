# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok

from p2.datashackle.core.interfaces import IWidgetType
from p2.datashackle.management.views import AjaxView, BaseView



class Widget(BaseView):
    grok.name('widget')
    grok.context(IWidgetType)

    template = grok.PageTemplateFile('widget.pt')

    def update(self):
        if self.request.form.get('mode') == 'ARCHETYPE':
            self.source_id = self.request.form['source_id']
        else:
            self.source_id = self.context.form.collections['widgets']['collection_id']
    
   
class ArchetypeWidget(AjaxView, Widget):
    grok.name('archetypewidget')
    
    def update(self):
        AjaxView.update(self)
        Widget.update(self)

