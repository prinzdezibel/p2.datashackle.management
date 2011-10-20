# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok

from zope.component import getUtility, getMultiAdapter

from p2.datashackle.core.interfaces import *
from p2.datashackle.management.views import BaseView


class Span(BaseView):
    grok.name('span')
    grok.context(ISpanType)
    source_id = None

    def update(self):
        if self.context.operational:
            self.source_id = self.request.form.get('source_id')
        elif self.request.form.get('mode') == 'ARCHETYPE':
            self.source_id = self.request.form['source_id']
        else:
            self.source_id = self.context.widget.collections['spans']['collection_id']

    def render(self):
        self.template = grok.PageTemplateFile(self.template_name.lower() + '.pt')
        return self._render_template()

