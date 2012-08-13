# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>


import grok

from zope.component import queryMultiAdapter

from p2.datashackle.core.interfaces import IFormType
from p2.datashackle.management.form.views.base import BaseForm
    

class DataManagementView(BaseForm):
    template = grok.PageTemplateFile('../templates/tablerowform.pt')
    grok.name("tablerowform")
    grok.context(IFormType)

    def call_form(self):
        self.request.form['source_id'] = self.source_id
        form = queryMultiAdapter((self.context, self.request), name='changeableform')
        self.request.form['mode'] = self.mode
        self.request.form['setobject_id'] = self.context.op_setobject_id
        self.request.form['alternation'] = None
        form.source_id = self.request.form['source_id']
        return form()

    def update(self):
        super(DataManagementView, self).update()
        form = self.request.form
        if 'runtimecreated' in form:
            self.runtimecreated = True
        else:
            self.runtimecreated = False

