# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Jonas Thiem <jonas.thiem%40projekt-und-partner.com>

import grok, grokcore

from zope.component import getUtility, getMultiAdapter

from p2.datashackle.core.interfaces import ISimpleSQLSearch, IPlan
from p2.datashackle.management.interfaces import IGenericSet


class SearchbackendView(grok.View):
    grok.context(IGenericSet)
    grok.name("searchbackend")
    grok.order(15)
    grok.require('dolmen.content.View')
   
    def call_form(self, setobject_id):
        form = self.context.plan.default_form
        if form == None:
            form = self.context.plan.forms.values()[0]
        form_view = getMultiAdapter((form, self.request), name='tablerowform') 
        form_view.request.form['setobject_id'] = setobject_id
        form_view.request.form['mode'] = 'OPERATIONAL'
        return form_view()
    
    def update(self):
        self.searchresults = []
        self.searched = False
        self.currentpage = 1
        self.nextpage = False
        form = self.request.form
        if 'q' in form and 'p' in form:
            try:
                page = int(form['p'])
            except:
                return
            if (page < 1):
                page = 1
            # do the search and prepare the data
            util = getUtility(ISimpleSQLSearch)
            results = util.do(self.context.plan, form['q'], "", page, 5)
            self.searched = True
            if results['resultset']:
                for result in results['resultset']:
                    # prepare searchresults for the template
                    # we probably just want to know which fields are highlighted and somehow pass this to the form
                    # ... (fixme)
                    # then we prepare the form for this specific dataset:
                    self.searchresults.append({'setobject_id': result.values()[0]})
            self.nextpage = results['nextpage']
            self.currentpage = page
        return
         
    def render(self):
        template = grokcore.view.PageTemplateFile("../templates/searchrequestbackend.pt")
        html = template.render(self)
        return html
