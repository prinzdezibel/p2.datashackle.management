# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok

from p2.datashackle.management.interfaces import IWidgetType
from p2.datashackle.management.views import BaseView

from p2.datashackle.management.setobject_graph import SetobjectGraph
from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.core.interfaces import IDbUtility
from zope.component import getUtility


class Widget(BaseView):
    grok.name('widget')
    grok.context(IWidgetType)

    template = grok.PageTemplateFile('widget.pt')

    def update(self):
        if self.request.form.get('mode') == 'ARCHETYPE':
            self.source_id = self.request.form['source_id']
        else:
            self.source_id = self.context.form.collections['widgets']['collection_id']
    
   
class ArchetypeWidget(BaseView):
    grok.name('archetypewidget')
    grok.context(IWidgetType)

    template = grok.PageTemplateFile('widget.pt')

    def update(self):
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
            classname = self.context.op_setobject_type.__name__
        elif self.mode == 'DESIGNER' or self.mode == 'ARCHETYPE':
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
            graph.link(self.source_id, classname, setobject_id, self.linked)
            
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
   
        self.context = self.setobject
        




