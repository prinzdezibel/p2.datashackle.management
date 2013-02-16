# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2011
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok

from zope.component import getUtility, getMultiAdapter
from zope.interface import Interface, Attribute

from p2.datashackle.core.interfaces import IDbUtility, ILocationProvider
from p2.datashackle.management.views import AjaxView
from p2.datashackle.management.interfaces import IFormType
            
       
class BaseForm(AjaxView):
    grok.context(IFormType)
    template = grok.PageTemplateFile('../templates/baseform.pt')

    def __init__(self, context, request):
        super(BaseForm, self).__init__(context, request)
        self.plan_id = self.context.plan.plan_identifier    
        self.extra_classes = ''
 
    def update(self):
        super(BaseForm, self).update()
        alternation = self.request.form.get('alternation')
        if alternation:
            self.extra_classes += ' ' + alternation
        if self.request.form.get('show_strip') == 'true':    
            self.extra_classes += ' selector-strip'

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
