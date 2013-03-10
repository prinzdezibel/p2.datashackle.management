# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2011
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok

from zope.component import getUtility, getMultiAdapter
from zope.interface import Interface, Attribute

from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.management.views import AjaxView
from p2.datashackle.management.interfaces import IFormType

from zeam.form.base import Action, Actions
from zeam.form.base import Form as StandaloneForm
from zeam.form.layout import Form as LayoutAwareForm

from p2.datashackle.core.models.identity import generate_random_identifier
from p2.datashackle.management.setobject_graph import SetobjectGraph
from p2.datashackle.core.app.setobjectreg import setobject_type_registry


class FormMixin(object):
    grok.context(IFormType)
    setobject = None

    extra_classes = ''

    @property
    def plan_id(self):
        return self.context.plan.plan_identifier
 
    @property
    def prefix(self):
        return str(self.context.form_identifier)

    def generate_random_identifier(self):
        return generate_random_identifier()

    def render(self):
        self.mode = self.request.form.get('mode')
        setobject_id = self.request.form.get('setobject_id')
        self.graph_xml = self.request.form.get('graph')
        if self.graph_xml != None:
            del(self.request.form['graph'])
        self.source_id = self.request.form.get('source_id')
        if self.source_id != None:
            # Delete request's source_id, as subforms should not see it.
            del(self.request.form['source_id'])
    	self.linked = self.request.form.get('linked')
        if self.linked != None:
            del(self.request.form['linked'])
        if self.linked != None and self.linked != 'true' and self.linked != 'false':
    	    raise Exception("Invalid value for parameter linked")
    	if self.source_id != None and self.linked == None:
    		raise Exception("source_id parameter must be accompanied by linked parameter")
    	if self.linked != None and self.source_id == None:
            raise Exception("linked parameter must be accompanied by linked source_id parameter.")
    	self.relation_source_id = self.request.form.get('relation_source_id')
        
        db_utility = getUtility(IDbUtility)
        session = db_utility.Session()
      
        if self.mode == 'OPERATIONAL':
            module = self.context.op_setobject_type.__module__
            classname = self.context.op_setobject_type.__name__
        elif self.mode == 'DESIGNER' or self.mode == 'ARCHETYPE':
            module = self.context.__module__
            classname = self.context.__class__.__name__
        else:
             raise Exception("Mode must have one of the values ARCHETYPE, DESIGNER, OPERATIONAL")
        
        self.klass = setobject_type_registry.lookup(classname)
        if not setobject_id:
            setobject = self.klass()
            session.add(setobject)
            setobject_id = setobject.id
            session.flush()
        
        if self.graph_xml != None and self.graph_xml != '':
            graph = SetobjectGraph(self.request, self.graph_xml)        
            graph.link(self.source_id, module, classname, setobject_id, self.linked)
            
        if setobject_id != None:
            self.setobject = session.query(self.klass).filter(self.klass.get_primary_key_attr() == setobject_id).one()
        
        relation_id = self.request.get('relation_id')
        if relation_id != None:
            if self.relation_source_id == None:
                raise Exception("relation_id parameter must be accompanied by relation_source_id.")
            self.relation = session.query(EmbeddedForm).filter_by(span_identifier=relation_id).one()
            source_type = setobject_type_registry.lookup(self.relation.linkage.source_model.klass)
            self.relation_source = session.query(source_type).filter(source_type.get_primary_key_attr() == self.relation_source_id).one()   
        
        if self.graph_xml != None and self.graph_xml != '':
            # Each query after graph.link() call might generate new dynamic linkage id's. Correct them if necessary.
            graph.update_collections()
            
        alternation = self.request.form.get('alternation')
        if alternation:
            self.extra_classes += ' ' + alternation
        if self.request.form.get('show_strip') == 'true':    
            self.extra_classes += ' selector-strip'

        if self.mode == 'OPERATIONAL' and self.setobject != None:
            self.context = self.context.make_operational(self.setobject)
        template = grok.PageTemplateFile('../templates/baseform.pt')
        return template.render(self)

    def render_widgets(self):
        from p2.datashackle.core.models.browser.scopedmarkup import ScopedMarkup
        i = ScopedMarkup()
        for widget in self.context.widget_collection():
            view = widget.lookup_view(self.request, self.mode)
            i.html(view())
        html = i.render()
        return html


class BaseForm(FormMixin, StandaloneForm):
    pass

class LayoutAwareForm(FormMixin, LayoutAwareForm):
    pass

#class SaveForm(grok.View):
#    grok.context(IFormType)
#
#    def __init__(self, context, request):
#        super(SaveForm, self).__init__(context, request)
#        if self.request.environment.get('X-Requested-With') == 'XMLHttpRequest':
#            self.ajax = True
#            self.response.setHeader('Content-Type', 'application/json')
#        else:
#            self.ajax = False
#
#    def update(self):
#        graph_xml = self.request.form['data']
#        graph = SetobjectGraph(self.request, graph_xml)
#        self.result = graph.save()
#
#    def render(self):
#        if self.ajax:
#            return self.result
#        else:
            
        
class DesignerForm(BaseForm):
    class SaveAction(Action):
        def __call__(self, form):
            import pdb; pdb.set_trace()
    
    actions = Actions(SaveAction('save'),)

