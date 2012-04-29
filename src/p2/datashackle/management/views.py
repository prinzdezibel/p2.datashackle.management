# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
import urllib, urllib2
import logging
import json
from urlparse import urlparse

from zope.app.appsetup.product import getProductConfiguration
from zope.component import getUtility
from zope.publisher.publish import mapply

from grokcore.view.components import View
from zope.app.appsetup.product import getProductConfiguration

from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.management.interfaces import IDatashackle
from p2.datashackle.core.app.exceptions import SetobjectGraphException, UserException
from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.core.models.identity import generate_random_identifier
from p2.datashackle.management.span.embeddedform import EmbeddedForm
from p2.datashackle.management.setobject_graph import SetobjectGraph


class BaseView(grok.View):
    grok.baseclass()

    def generate_random_identifier(self):
        return generate_random_identifier()

class AjaxView(BaseView):
    grok.baseclass()

    setobject = None  
 
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
            module = self.context.op_setobject_type.__module__
            classname = self.context.op_setobject_type.__name__
        elif self.mode == 'DESIGNER' or self.mode == 'ARCHETYPE':
            module = self.context.__module__
            classname = self.context.__class__.__name__
        else:
             raise Exception("Mode must have one of the values ARCHETYPE, DESIGNER, OPERATIONAL")
        
        self.so_type = setobject_type_registry.lookup(module, classname)
        if setobject_id == '':
            setobject = self.so_type()
            session.add(setobject)
            setobject_id = setobject.id
            session.flush()
        
        if self.graph_xml != None and self.graph_xml != '':
            graph = SetobjectGraph(self.request, self.graph_xml)        
            graph.link(self.source_id, module, classname, setobject_id, self.linked)
            
        if setobject_id != None:
            self.setobject = session.query(self.so_type).filter(self.so_type.get_primary_key_attr() == setobject_id).one()
        
        relation_id = self.request.get('relation_id')
        if relation_id != None:
            if self.relation_source_id == None:
                raise Exception("relation_id parameter must be accompanied by relation_source_id.")
            self.relation = session.query(EmbeddedForm).filter_by(span_identifier=relation_id).one()
            source_type = setobject_type_registry.lookup(self.relation.linkage.source_module, self.relation.linkage.source_classname)
            self.relation_source = session.query(source_type).filter(source_type.get_primary_key_attr() == self.relation_source_id).one()   
        
        if self.graph_xml != None and self.graph_xml != '':
            # Each query after graph.link() call might generate new dynamic linkage id's. Correct them if necessary.
            graph.update_collections()
        

class JsonView(grok.View):
    grok.baseclass() 
    
    def __call__(self):
        self.response.setHeader('Content-Type', 'application/json')
       
        # When configured appropriately, loop request through nodejs scripting server. 
        config = getProductConfiguration('setmanager')
        if config['nodeserver_scripting'].lower() == 'on':
            result = self.before_update_hook()
            if result != None:
                # Send response
                return result

        try:
            mapply(self.update, (), self.request)
        except SetobjectGraphException as e:
            return json.dumps({'error': {'message': e.reason,
                                         'id': e.setobjectid,
                                         'title': "Error during submit"}})
        
        except UserException as e:
            return json.dumps({'error': {'message':str(e),
                                         'title': "Error"}})
                                         
        if self.request.response.getStatus() in (302, 303):
            # A redirect was triggered somewhere in update().  Don't
            # continue rendering the template or doing anything else.
            return

        template = getattr(self, 'template', None)
        if template is not None:
            return self._render_template()

        return mapply(self.render, (), self.request) 

    def before_update_hook(self):
        """Before update happens, setmanager does a RPC call to the node.js Server.
        The call is mapped onto an optionally (user-defined) Javascript function.
        If a plugin is found, the function is executed. If not, the standard
        grok behaviour takes place.
        """
        
        jsonrpc_method = 'beforeUpdate'
        # ES5 specification requires all JSON strings to be enclosed in double quotes.
        # This requires to be all literal " that appear in the xml to be escaped
        data = self.request.form['root'].replace('"', '\\"')
        # JSON strings may not contain unescaped newlines
        data = data.replace('\n', '\\n')
        jsonrpc_params = {'root': data}        
 
        body =  '{"jsonrpc": "2.0",'
        body += '"id": "false",'
        body += '"method": "' + jsonrpc_method + '",'
        body += '"params": [{'
        body += ','.join(['"%s": "%s"' % (k,v) for (k,v) in jsonrpc_params.items()])
        body += '}]}'
 
        config = getProductConfiguration('setmanager')
        host = config['node_host']
        port = config['node_port']
        node_root = config['node_root']

        url = 'http://' + host
        if len(port) > 0:
            url += ':' + port
        path = urlparse(self.request.getURL())[2]
        # strip the part that contains the zope application
        index = path.index('/', 1)
        path = path[index:]
        # remove @@
        index = path.find('@@')
        if index > 0:
            path = path[:index] + path[index + 2:]
        # remove traversal adapter ++view++
        index = path.find('++view++')
        if index > 0:
            path = path[:index] + path[index + 8:]
        url += path
        
        # Certain values that serve as environment within a node.js request
        # are sent as query parameters.
        db_util = getUtility(IDbUtility)
        conn = db_util.getConnectionString()
        params = dict(conn=conn, node_root=node_root)                
        url += '?'
        url += "&".join(["%s=%s"%(k,v) for (k,v) in params.items()])       
        
        # The RPC call
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url, body, headers)
        try:
            # ATM, the timeout for request is 1 second.
            response = urllib2.urlopen(request, None, 1)
        except urllib2.HTTPError as e:
            # 40X or 50X errors
            # error property in json response will be filled according to JsonRPC specification.
            response = e.read()
            data = json.loads(response)
            logging.error('Node.js server returned error code %s: %s' % (e.getcode(), data['error']['message']))
            return json.dumps({'error': {'message': data['error']['message'],
                                         'title': 'HTTP Error %s' % e.code}})
        except urllib2.URLError as e:
            # Often, URLError is raised because there is no network connection (no route to the specified server),
            # or the specified server doesn't exist
            logging.error('Node.js server call failed: %s' % str(e.reason))
            return json.dumps({'error': {'message': e.reason,
                                         'title': "Network error"}});
                                         
           
        json_string = response.read()
        data = json.loads(json_string)
        if 'error' in data['result']:
            return json.dumps({'error': data['result']['error']})
        else:
            # Re-assign returned values 
            self.request.form['root'] = data['result']['params']['root'] 

        # proceed with request
        return None
        
