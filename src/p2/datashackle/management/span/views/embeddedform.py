# -*- coding: utf-8 -*-
# Copyright (C), projekt-und-partner.com, 20111
# Author: Michael Jenny

import grok

from zope.component import getMultiAdapter, getUtility
from zope.traversing.browser import absoluteurl

from p2.datashackle.core.interfaces import ISpanType, ILocationProvider
from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.management.relation import RelationMixin, QueryMode
from p2.datashackle.management.span.views.span import Span

class EmbeddedForm(Span, RelationMixin):
    grok.name('embeddedform')
    grok.context(ISpanType)

    def __init__(self, context, request):
        Span.__init__(self, context, request)
        RelationMixin.__init__(self, show_strip=False)
    
    def update(self):
        Span.update(self)
        if self.context.operational:
            self.relation_source = self.context.setobject
            self.relation = self.context
            RelationMixin.update(self)
        self.targetResource = ''
        if self.context.operational:
            self.query = self.query_related(query_mode=QueryMode.EXCLUSIVE, filter_clause=self.relation.filter_clause)
            self.count = self.query.count()
            target_form = self.context.form_name
            target_plan = self.context.plan_identifier
            util = getUtility(ILocationProvider)
            genericset = util.lookup_genericset(target_plan)
            form = genericset.plan.forms[target_form]
            self.targetResource = absoluteurl.absoluteURL(form, self.request)
           
    def render(self):
        self.template = grok.PageTemplateFile('embeddedform.pt')
        return self._render_template()
