# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2011
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
import json

from zope.component import getUtility, getMultiAdapter
from zope.interface import Interface, Attribute

from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.management.interfaces import IFormType

from zeam.form.base import Action, Actions

from p2.datashackle.core.models.identity import generate_random_identifier
from p2.datashackle.management.setobject_graph import SetobjectGraph
from p2.datashackle.core.app.setobjectreg import setobject_type_registry

from zope.publisher.publish import mapply

from zeam.form.base import Form as ZeamForm
from zope import i18n

from grokcore.layout.interfaces import ILayout, IPage
from zope.component import getMultiAdapter
from zeam.form.layout.form import LayoutAwareForm as ZeamLayoutAwareForm

   
class FormTemplateFile(grok.PageTemplateFile):
    def render(self, view):
        view.mode = view.request.form.get('mode')
        setobject_id = view.request.form.get('setobject_id')
        view.graph_xml = view.request.form.get('graph')
        if view.graph_xml != None:
            del(view.request.form['graph'])
        view.source_id = view.request.form.get('source_id')
        if view.source_id != None:
            # Delete request's source_id, as subforms should not see it.
            del(view.request.form['source_id'])
    	view.linked = view.request.form.get('linked')
        if view.linked != None:
            del(view.request.form['linked'])
        if view.linked != None and view.linked != 'true' and view.linked != 'false':
    	    raise Exception("Invalid value for parameter linked")
    	if view.source_id != None and view.linked == None:
    		raise Exception("source_id parameter must be accompanied by linked parameter")
    	if view.linked != None and view.source_id == None:
            raise Exception("linked parameter must be accompanied by linked source_id parameter.")
    	view.relation_source_id = view.request.form.get('relation_source_id')
        
        db_utility = getUtility(IDbUtility)
        session = db_utility.Session()
      
        if view.mode == 'OPERATIONAL':
            classname = view.context.op_setobject_type.__name__
        elif view.mode == 'DESIGNER' or view.mode == 'ARCHETYPE':
            classname = view.context.__class__.__name__
        else:
             raise Exception("Mode must have one of the values ARCHETYPE, DESIGNER, OPERATIONAL")
        
        view.klass = setobject_type_registry.lookup(classname)
        if not setobject_id:
            setobject = view.klass()
            session.add(setobject)
            setobject_id = setobject.id
            session.flush()
        
        if view.graph_xml != None and view.graph_xml != '':
            graph = SetobjectGraph(view.request, view.graph_xml)        
            graph.link(view.source_id, classname, setobject_id, view.linked)
            
        if setobject_id != None:
            view.setobject = session.query(view.klass).filter(view.klass.get_primary_key_attr() == setobject_id).one()
        
        relation_id = view.request.get('relation_id')
        if relation_id != None:
            if view.relation_source_id == None:
                raise Exception("relation_id parameter must be accompanied by relation_source_id.")
            view.relation = session.query(EmbeddedForm).filter_by(span_identifier=relation_id).one()
            source_type = setobject_type_registry.lookup(view.relation.linkage.source_model.klass)
            view.relation_source = session.query(source_type).filter(source_type.get_primary_key_attr() == view.relation_source_id).one()   
        
        if view.graph_xml != None and view.graph_xml != '':
            # Each query after graph.link() call might generate new dynamic linkage id's. Correct them if necessary.
            graph.update_collections()
            
        alternation = view.request.form.get('alternation')
        if alternation:
            view.extra_classes += ' ' + alternation
        if view.request.form.get('show_strip') == 'true':    
            view.extra_classes += ' selector-strip'

        if view.mode == 'OPERATIONAL' and view.setobject != None:
            view.context = view.context.make_operational(view.setobject)
        
        return super(FormTemplateFile, self).render(view)
        

class FormManager(grok.ViewletManager):
    grok.name('form')
    grok.context(IFormType)

class FormViewlet(grok.Viewlet):
    grok.viewletmanager(FormManager)
    grok.context(IFormType)
    grok.order(0)
    
    def render(self, *args, **kwargs):
        self.template = grok.PageTemplateFile('templates/form.pt')
        return super(FormViewlet, self).render(*args, **kwargs)

class Form(ZeamForm):
    grok.context(IFormType)
    setobject = None
    grok.baseclass()
    extra_classes = ''

    @property
    def plan_id(self):
        return self.context.plan.plan_identifier
 
    @property
    def prefix(self):
        return str(self.context.form_identifier)

    def generate_random_identifier(self):
        return generate_random_identifier()

    def render_widgets(self):
        from p2.datashackle.core.models.browser.scopedmarkup import ScopedMarkup
        i = ScopedMarkup()
        for widget in self.context.widget_collection():
            view = widget.lookup_view(self.request, self.mode)
            i.html(view())
        html = i.render()
        return html

class BareForm(Form):
    grok.name("bareform")

    def render(self):
        template = FormTemplateFile('templates/bareform.pt')
        return template.render(self)


class LayoutAwareForm(ZeamLayoutAwareForm, Form):
    grok.implements(IPage)
    grok.name('layoutawareform')

    layout = None

    template = FormTemplateFile('templates/bareform.pt')

    def default_namespace(self):
        namespace = super(LayoutAwareForm, self).default_namespace()
        namespace['layout'] = self.layout
        return namespace

    def content(self):
        return self.template.render(self)

    def __call__(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            # A redirect was triggered somewhere in update().  Don't
            # continue processing the form
            return
        self.updateForm()
        if self.request.response.getStatus() in (302, 303):
            return

        self.layout = getMultiAdapter(
            (self.request, self.context), ILayout)
        return self.layout(self)


class DesignerForm(Form):
    class SaveAction(Action):
        def __call__(self, form):
            graph_xml = form.request.form['data']
            graph = SetobjectGraph(form.request, graph_xml)
            result = graph.save()
            form.saved = True

    grok.name("designerform")
    actions = Actions(SaveAction('save'),)
    saved = False

    def render(self):
        if self.saved:
            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps({})
        else:
            template = FormTemplateFile('templates/designerform.pt')
            return template.render(self)
 



