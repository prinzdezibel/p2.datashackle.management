# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>


import grok

from zope.component import queryMultiAdapter

from p2.datashackle.management.interfaces import IFormType
from p2.datashackle.management.form.views.base import Form

from p2.datashackle.management.form.views.base import FormTemplateFile
    
class DataManagementView(Form):
    grok.name("tablerowform")

    def render(self):
        template = FormTemplateFile('templates/tablerowform.pt')
        return template.render(self)

    def update(self):
        super(DataManagementView, self).update()
        form = self.request.form
        if 'runtimecreated' in form:
            self.runtimecreated = True
        else:
            self.runtimecreated = False
       
        #import pdb; pdb.set_trace() 
        #self.request.form['changeableform'] = True
        #self.request.form['mode'] = self.mode
        #self.request.form['setobject_id'] = self.context.op_setobject_id
        #self.request.form['alternation'] = None

