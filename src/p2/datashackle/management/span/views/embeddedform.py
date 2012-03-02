# -*- coding: utf-8 -*-
# Copyright (C), projekt-und-partner.com, 20111
# Author: Michael Jenny

import grok

from sqlalchemy.sql.expression import literal_column
from zope.component import getMultiAdapter, getUtility
from zope.traversing.browser import absoluteurl


from p2.datashackle.core import Session
from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.core.interfaces import ISpanType, ILocationProvider
from p2.datashackle.management.relation import RelationMixin, QueryMode
from p2.datashackle.management.views import AjaxView
from p2.datashackle.management.span.views.span import Span


class EmbeddedForm(Span, RelationMixin):
    grok.name('embeddedform')
    grok.context(ISpanType)

    def __init__(self, context, request):
        Span.__init__(self, context, request)
        RelationMixin.__init__(self, show_strip=False)
    
    def update(self):
        Span.update(self)
        self.targetResource = ''
        name = grok.name.bind().get(self.__class__)
        self.treequery_url = grok.url(self.request, self.context) + \
            '/@@treequery?mode=OPERATIONAL'
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


class TreeQuery(AjaxView):
    grok.name('treequery')
    grok.context(ISpanType)
    template = grok.PageTemplateFile('embeddedform_treequery.pt')
    
    def update(self):
        super(TreeQuery, self).update()
        # View only suitable for adjacency lists
        assert(self.context.characteristic.id == 'ADJACENCY_LIST')
        self.node_id = self.request.form.get('node_id', None)
        
        session = Session()
        plan_id = self.context.plan_identifier
        from p2.datashackle.management.plan.plan import Plan
        plan = session.query(Plan).get(plan_id)
        target_type = setobject_type_registry.lookup(plan.so_module, plan.so_type)        
        query = session.query(target_type)
        query = query.add_column(
            literal_column("'false'").label('linked')
        )
        linkage_id = self.context.adjacency_linkage
        from p2.datashackle.core.models.linkage import Linkage
        linkage = session.query(Linkage).get(linkage_id)
        self.adjacency_attr_name = linkage.attr_name
        query = query.filter(getattr(target_type, linkage.relation.foreignkeycol) == self.node_id)
        if self.context.filter_clause:
            query = query.filter(self.context.filter_clause)
        self.count = query.count()
        self.query = query

    def call_subform(self, source_id, setobject_id):
        # Fetch the right form with correct location information.
        # (use genericset)
        form = None
        plan_identifier = self.context.plan_identifier
        form_name = self.context.form_name
        util = getUtility(ILocationProvider)
        genericset = util.get_genericset(plan_identifier)
        form = genericset.plan.forms[form_name]
        
        form_view = getMultiAdapter((form, self.request), name='baseform')
        self.request.form['source_id'] = source_id
        self.request.form['setobject_id'] = setobject_id
        self.request.form['mode'] = 'OPERATIONAL'
        self.request.form['linked'] = source_id and 'true' or None
        self.request.form['show_strip'] = 'false'
         
        return form_view()
