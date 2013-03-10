# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Jonas Thiem <jonas.thiem%40projekt-und-partner.com>


import grok

from zope.component import queryMultiAdapter

from p2.datashackle.management.interfaces import IFormType
from p2.datashackle.management.form.views.base import BaseForm
    

#class ChangeableForm(BaseForm):
class ChangeableForm(grok.View):
    template = grok.PageTemplateFile('../templates/changeableform.pt')
    grok.name("changeableform")
    grok.context(IFormType)

    def call_form(self):
        form = queryMultiAdapter((self.context, self.request), name='baseform')
        self.request.form['changeableform'] = True
        return form()
