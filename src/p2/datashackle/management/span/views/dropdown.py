# -*- coding: utf-8 -*-
# Copyright (C), projekt-und-partner.com, 2011
# Author: Michael Jenny

import grok

from zope.component import getMultiAdapter, getUtility
from zope.traversing.browser import absoluteurl

from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.management.relation import RelationMixin, QueryMode
from p2.datashackle.management.span.views.span import Span
from p2.datashackle.management.interfaces import ISpanType


class Dropdown(Span, RelationMixin):
    grok.name('dropdown')
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
            self.query = super(Dropdown, self).query(query_mode=QueryMode.SHARED)
            self.count = self.query.count()
            # Is already an item selected?
            self.selected = False
            for (_, linked) in self.query:
                if linked == 'true':
                    self.selected = True
                    break
    
    def render(self):
        self.template = grok.PageTemplateFile('dropdown.pt')
        return self._render_template()
