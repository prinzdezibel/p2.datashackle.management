# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2011
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok

from zope.component import getUtility, getMultiAdapter
from zope.interface import Interface, Attribute

from p2.datashackle.core.interfaces import IFormType, IDbUtility, ILocationProvider
from p2.datashackle.management.views import AjaxView

            
       
class BaseForm(AjaxView):
    grok.context(IFormType)
    template = grok.PageTemplateFile('../templates/baseform.pt')
    strip_width = 15

    def __init__(self, context, request):
        super(BaseForm, self).__init__(context, request)
        self.plan_id = self.context.plan.plan_identifier    
    
    def update(self):
        super(BaseForm, self).update()
        self.alternation = self.request.form.get('alternation')
        self.style = 'position: relative;'
        show_strip = self.request.form.get('show_strip')
        if show_strip == 'true':
            self.style += 'left: ' + str(self.strip_width) + 'px;'
            self.style += 'width: ' + str(self.context.width + self.strip_width) + 'px;'
        else:
            self.style += 'width: ' + str(self.context.width) + 'px;'
        self.style += 'height: ' + str(self.context.height) + 'px;'
        if self.mode == 'OPERATIONAL' and self.setobject != None:
            self.context = self.context.make_operational(self.setobject)

    def render_widgets(self):
        from p2.datashackle.core.models.browser.scopedmarkup import ScopedMarkup
        i = ScopedMarkup()
        for widget in self.context.widget_collection():
            view = widget.lookup_view(self.request, self.mode)
            i.html(view())
        html = i.render()
        return html
