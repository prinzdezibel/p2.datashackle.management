# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>


import grok
import json

from lxml import etree
from zope.component import getUtility

from p2.datashackle.core.interfaces import IGenericSet
from p2.datashackle.core.app.exceptions import UnspecificException, SetobjectGraphException
from p2.datashackle.core.interfaces import IGenericSet
from p2.datashackle.core.models.setobject_graph import SetobjectGraph
from p2.datashackle.management.views import JsonView


class CommitToServer(JsonView):
    grok.context(IGenericSet)
    grok.name("committoserver");
    
    def update(self):
        self.jsonresponse = dict()
        if self.request.form.get('graph') == None or (len(self.request.form['graph']) == 0):
            raise UnspecificException("No data transmitted.")

        graph_xml = self.request.form['graph']

        try:
            graph = SetobjectGraph(self.context.plan.plan_identifier, self.request, graph_xml)
            graph.save()
            self.jsonresponse['result'] = 'OK'
        except SetobjectGraphException, ex:
            self.jsonresponse['error'] = {'title': 'Save failed',
                                      'message': ex.reason,
                                      'data_node_id': ex.setobjectid}

    def render(self):
        return json.dumps(self.jsonresponse)    
