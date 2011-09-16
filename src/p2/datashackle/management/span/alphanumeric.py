# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2011
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok

from zope.component import getUtility, getMultiAdapter

from p2.datashackle.core.interfaces import *
from p2.datashackle.management.scopedmarkup import ScopedMarkup
from p2.datashackle.management.views import BaseView
from p2.datashackle.management.span.span import Span


class Alphanumeric(Span):
    grok.name('alphanumeric')
    grok.context(ISpanType)
    
    def render(self):
        id = self.generate_random_identifier()
        i = ScopedMarkup()
        i.html('<div class="p2-span" id="%s" data-span-type="%s" data-field-identifier="%s" style="%s">' % (
            id,
            self.context.span_type,
            self.context.field_identifier,
            self.context.css_style
        ))
        i.script('var info = $.parseJSON(%s);' % i.literal(self.context.get_info()))
        if self.source_id != None:
            i.script('var sourceId = \'%s\';' % self.source_id)
        else:
            i.script('var sourceId = null;')
        i.script('$(\'#%s\').data(\'data-object\', new p2.Span.Alphanumeric($(\'#%s\'), sourceId, \'%s\', info));' % (id, id, self.application_url()))
        i.html('</div>')
        html = i.render()
        return html


