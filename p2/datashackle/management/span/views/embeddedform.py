# -*- coding: utf-8 -*-
# Copyright (C), projekt-und-partner.com, 20111
# Author: Michael Jenny

import grok

from sqlalchemy.sql.expression import literal_column
from zope.component import getMultiAdapter, getUtility
from zope.traversing.browser import absoluteurl


from p2.datashackle.core import Session
from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.management.relation import RelationMixin, QueryMode
from p2.datashackle.management.span.views.span import Span
from p2.datashackle.management.interfaces import ISpanType, ILocationProvider



class EmbeddedForm(Span, RelationMixin):
    grok.name('EmbeddedForm')
    grok.context(ISpanType)

    def __init__(self, context, request):
        Span.__init__(self, context, request)
        RelationMixin.__init__(self, show_strip=False)
 
    def update(self):
        Span.update(self)
        self.targetResource = ''
        name = grok.name.bind().get(self.__class__)
        if self.context.operational:
            self.relation_source = self.context.setobject
            self.relation = self.context
            RelationMixin.update(self)
        
            self.query = super(EmbeddedForm, self).query(
                query_mode=QueryMode.EXCLUSIVE
            )

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
