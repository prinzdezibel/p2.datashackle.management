# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2011
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok

from zope.component import getUtility

from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.core.interfaces import IFormType, IDbUtility
from p2.datashackle.management.relation import RelationMixin, QueryMode
from p2.datashackle.management.scopedmarkup import ScopedMarkup
from p2.datashackle.management.form.base import BaseForm
from p2.datashackle.core.models.identity import generate_random_identifier
from p2.datashackle.core.models.span.relation import Relation
 
 
grok.templatedir('templates')

        

class ObjectPicker(BaseForm, RelationMixin):

    grok.context(IFormType)
    template = None

    def __init__(self, context, request):
        BaseForm.__init__(self, context, request)
        RelationMixin.__init__(self, show_strip=True)

    def update(self):
        BaseForm.update(self)
        RelationMixin.update(self)
       
    def render(self):
        relation_id = self.relation.id
        i = ScopedMarkup()
        i.script('var objectPicker = new p2.ObjectPicker(\'%s\', \'%s\', %s, \'%s\');' % (
            self.relation_source.id,
            relation_id,
            self.is_multi_selectable and 'true' or 'false',
            self.collection_id
        ))
        i.html('<div style="position: relative">')
        a = 0
        query = self.query_related()
        for (setobject, linked) in query:
            alternation = a%2 == 0 and 'even' or 'odd'
            a += 1
            id = generate_random_identifier()
            i.html("""
                   <div style="position:absolute; z-index:10000;">
                        <input id="%s" value="%s" type="checkbox" />
                   </div>
                   """ % (id, setobject.id))
            subform = self.call_subform(self.collection_id ,setobject.id, linked, alternation)
            subform = subform.replace(r'\"', r'\\\"')
            i.html(subform)
            i.html('</div>')
            i.script('objectPicker.registerCheckbox($(\'#%s\'), %s)' % (id, linked)) 
        html = i.render()
        return html
