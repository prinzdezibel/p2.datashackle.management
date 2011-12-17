// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.SetobjectGraph");

p2.Edge = function(vertex){
    this.targetVertex = vertex;
    this.targetNode = undefined;
}

p2.GraphObject = function(vertex){
    this.vertex = vertex;
    this.adjacent = new Array();
    this.parent = null;
}

p2.SetobjectGraph = function(){
    this.init();
}

p2.SetobjectGraph.prototype.init = function(){
    this.vcount = 0;
    this.ecount = 0;
    this.adjlists = new Array();
}

p2.SetobjectGraph.prototype.insertVertex = function(vertex){
    // Only append once to adjlists
    if (this.queryGraphObject(vertex.id) != false) throw new Error("Vertex already exists in graph.");
    
    var adjlist = new p2.GraphObject(vertex);
    this.adjlists.push(adjlist);
    this.vcount++;
    
    //go through all graph nodes and see whether one of them has a target vertex that has not yet a node assigned
    for (var i = 0; i < this.adjlists.length; i++) {
        for (var k = 0; k < this.adjlists[i].length; k++) {
            var edge = this.adjlists[i][k];
            if (edge.targetVertex == vertex.id) {
                edge.targetNode = adjlist;
            }
        }
    }
    return adjlist;
}

p2.SetobjectGraph.prototype.getEdgeTargetNode = function(edge){
    if (edge.targetNode == undefined) {
        edge.targetNode = this.lookupGraphObject(edge.targetVertex.id);
    }
    return edge.targetNode;
}
p2.SetobjectGraph.prototype.lookupGraphObject = function(vertexId){
    for (var i = 0; i < this.adjlists.length; i++){
        if (this.adjlists[i].vertex.id == vertexId) return this.adjlists[i];
    }
    debugger;
    throw Error("Graph object not found.");
}

p2.SetobjectGraph.prototype.queryGraphObject = function(vertexId) {
    if (vertexId == undefined) {return false;}
    for (var i = 0; i < this.adjlists.length; i++){
        if (this.adjlists[i].vertex.id == vertexId) return this.adjlists[i];
    }
    return false;
}



p2.SetobjectGraph.prototype.edgeExists = function(sourceVertex, targetVertex){
    var adjlist = this.queryGraphObject(sourceVertex.id);
    for (var i = 0; i < adjlist.adjacent.length; i++){
        if(adjlist.adjacent[i].targetVertex.id == targetVertex.id) return true;
    }
    return false;
}

p2.SetobjectGraph.prototype._queryIncomingEdges = function(vertex){
    var incoming = [];
    for (var i = 0; i < this.adjlists.length; i++){
        var adjlist = this.adjlists[i];
        for (var a = 0; a < adjlist.adjacent.length; a++) {
            var targetVertex = adjlist.adjacent[a].targetVertex;
            if (targetVertex.id == vertex.id) {
                incoming.push(adjlist);
            }
        }
    }
    return incoming;
}

p2.SetobjectGraph.prototype._deleteGraphNode = function(node){
    var graph = this;
    var vertex = node.vertex;
    
    // delete child nodes
    while (node.adjacent.length > 0) {
        if (node.adjacent[0].targetNode == undefined) {
            node.adjacent[0].targetNode = graph.queryGraphObject(node.adjacent[0].targetVertex.id);
        }
        this._deleteGraphNode(node.adjacent[0].targetNode);
    }
    
    // check incoming edges from other vertexes.
    var incomingNodes = graph._queryIncomingEdges(vertex);
    for (var a = 0; a < incomingNodes.length; a++){
        // Delete the edge that refers to the target vertex that is about to be deleted.
        var incomingnode = incomingNodes[a];
        // delete edge from adjacency list
        for (var b = 0; b < incomingnode.adjacent.length; b++){
            if (incomingnode.adjacent[b].targetVertex.id == vertex.id){
                // Delete edge
                incomingnode.adjacent.splice(b, 1);
                // an edge between two nodes can only exist once.
                // It's safe to break out.
                break;
            }
        }
    }
    
    // delete node from graph
    for (var i = 0; i < graph.adjlists.length; i++) {
        adjlist = graph.adjlists[i];
        if (adjlist.vertex.id == vertex.id) {
            graph.adjlists.splice(i, 1);
            return;
        }
    }
}
p2.SetobjectGraph.prototype.deleteGraphObject = function(vertexId){
    var graph = this;
    // find target node to delete
    for (var i = 0; i < graph.adjlists.length; i++){
        var node = graph.adjlists[i];
        if (node.vertex.id == vertexId) {
            this._deleteGraphNode(node);
        }
    }
}

p2.SetobjectGraph.prototype.insertEdge = function(sourceVertexId, targetVertexId){
    // Check, if both vertexes exist.
    var sourceAdjlist = this.queryGraphObject(sourceVertexId);
    if (sourceAdjlist == false){debugger; throw new Error("sourceVertex " + sourceVertexId + " does not exist in graph.");}
    var sourceVertex = sourceAdjlist.vertex;
    
    var targetAdjlist = this.queryGraphObject(targetVertexId);
    if (targetAdjlist == false){debugger; throw new Error("targetVertex " + targetVertexId + " does not exist in graph.");}
    var targetVertex = targetAdjlist.vertex;

    if (sourceVertexId == targetVertexId){debugger; throw Error("Can't set an edge to myself!");}   

    if (sourceAdjlist.vertex instanceof p2.Setobject && targetAdjlist.vertex instanceof p2.Setobject)debugger;
 
    if (!this.edgeExists(sourceVertex, targetVertex)){
             
        // Put directed edge into graph
        sourceAdjlist.adjacent.push(new p2.Edge(targetVertex));

        // Set parent node for targetVertexId
        targetAdjlist.parent = sourceAdjlist;
    
        // check if newly created edge introduced a circle. This
        // is not a good thing to do. Remove the edge again.
        var parent = sourceAdjlist;
        while (parent = parent.parent){
            if (parent == targetAdjlist){
                // circle detected
                var index = sourceAdjlist.adjacent.length - 1;
                sourceAdjlist.adjacent.splice(index, 1);
                targetAdjlist.parent = null;
            }
        }    

        this.ecount++;
    }
}

p2.SetobjectGraph.prototype.toXmlFromVertex = function(root_vertex) {
    var vertex_is_ref = false; // root vertex is no ref to another vertex.
    var xmlDOM = this._dfsMain(root_vertex, vertex_is_ref);
    
    var xml = '';
    if (window.ActiveXObject){
        // code for IE
        xml = xmlDOM[0].xml;
    }else{
        // code for Mozilla, Firefox, Opera, etc.
        xml = (new XMLSerializer()).serializeToString(xmlDOM[0]);
    }
    return xml;
}

p2.SetobjectGraph.prototype.toXml = function(root_vertex_id) {
    if (root_vertex_id != null) {
        var adjlist = this.queryGraphObject(root_vertex_id);
        if (adjlist == false){debugger; throw new Error("Root vertex does not exist in graph.");}
        generatedxml = this.toXmlFromVertex(adjlist);
    }else{
        //cycle through all graph members and generate the xml for them
        generatedxml = "";
        var i = 0;
        while (i < this.adjlists.length) {
             // Other nodes that setobjects are ignored. E.g we are not interested in p2.CollectionVertex as standalone object.
             if (this.adjlists[i].vertex instanceof p2.Setobject) {
                if (this.adjlists[i].parent == null) {
                    if (this.adjlists[i].vertex.action != "ignore") {
                        if (generatedxml.length > 0) {generatedxml = generatedxml + "\n";}
                        generatedxml = generatedxml + this.toXmlFromVertex(this.adjlists[i]);
                    }
                }
            }
            i++;
        }
    }
    generatedxml = '<root version="1.0">\n' + generatedxml + '</root>\n';
    generatedxml = generatedxml.replace(/<([a-zA-Z0-9 ]+)\sxmlns=\"[^\"]*\"([^>]*)>/g, "<$1 $2>"); // remove the xmlns namespaces since we don't want them
    return generatedxml;
}

p2.SetobjectGraph.prototype.findRootVertex = function(vertexId){
    var go = this.queryGraphObject(vertexId);
    if (go == false) {throw new Error("Vertex " + vertexId + " does not exist in graph (findRootVertex).");}
    while (go.parent != null){
        go = go.parent;
    }
    return go.vertex;
}

// Depth first search algorithm is applied for serialization
p2.SetobjectGraph.prototype._dfsMain = function(adjlist, edge, node, nodeName) {
    // Pre-order xml generation
    var vertex_is_ref = edge.ref;
    var vertex = adjlist.vertex;
    
    var elem = null;
    if (node == null) {
       // 
       //  R O O T   N O D E
       //
       action = vertex.action;
       if (action == 'ignore') {
           action = 'save'; // we don't want to sent action ignore in that particular case
       }
       node = $.xmlDOM('<obj action="' + action + '" type="' + vertex.type + '" module="' + vertex.module + '"/>');
       elem = $(node).children();
    }else{
        if (vertex.action == 'ignore') {
            return node;
        }
        if (vertex instanceof p2.Setobject) {
            elem = $('<obj/>');
            if (nodeName){
                $(elem).attr('name', nodeName);
            }
            $(elem).attr('action', vertex.action);
            $(elem).attr('type', vertex.type);
            $(elem).attr('module', vertex.module);
            $(node).append(elem);
        }else if (vertex instanceof p2.LinkageVertex){
            if (vertex.refType == 'object'){
                // Embedded object, don't append this round.
                // Pass objects name to (the only) child element
                elem = node;
                nodeName = vertex.attrName;
            }else{
                // Collection type
                var coll = '<coll attr_name="' + vertex.attrName + '" linkage_id="' + vertex.id + '" ';
                if (vertex.spanIdentifier != null){
                    coll += 'span_identifier="' + vertex.spanIdentifier + '"';
                }
                coll += ' />';
                elem = $(coll);
                $(node).append(elem);
            }
        }
    }
    
    if (vertex instanceof p2.Setobject){
        $(elem).attr('objid', vertex.id);
        
        for (key in vertex.attrs){
           var attr = vertex.attrs[key];
           if (attr instanceof p2.Attribute){
               var prop = $('<prop/>');
               if (attr.spanIdentifier != null){
                   $(prop).attr('span_identifier', attr.spanIdentifier);
               }
               $(prop).attr('name', attr.name);
               $(prop).text(attr.value);
               $(elem).append(prop);
           }else{
               throw new Error('Invalid vertex attribute.');
           }
        }
    }

    for (var a = 0; a < adjlist.adjacent.length; a++){
        var edge = adjlist.adjacent[a];
        var adjacent_vertex = edge.targetVertex;
        var adjacent_adjlist = edge.targetNode;
        if (adjacent_adjlist == undefined) {
            adjacent_adjlist = this.queryGraphObject(edge.targetVertex.id);
        }
        this._dfsMain(adjacent_adjlist, edge, elem, nodeName);
    }

    // Set linkage information as post-processing step
    if (vertex instanceof p2.LinkageVertex){
        for (id in vertex.linkages){
            var obj =  $(elem).children('[objid="' + id + '"]');
            if (obj.length != 1){
                if (vertex.linkages[id] == 'true') {
                    debugger; throw Error("Linked p2.Setobject instance not found!");
                }
            }
            $(obj).attr('linked', vertex.linkages[id] ? 'true' : 'false');  
        }
    }
    return node; // return value only meaningful when function is called from outside this function (no recursion).
}
