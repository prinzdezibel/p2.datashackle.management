// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");


p2.Attribute = function(name, value, spanIdentifier){
    if (!name){debugger; throw Error("Name parameter is mandatory.")};
    this.spanIdentifier = spanIdentifier;
    this.name = name;
    this.value = value;
}

p2.LinkageVertex = function(id, attrName, isMultiSelectable, spanIdentifier){
    if (isMultiSelectable == null){debugger; throw Error("isMultiSelectable must be passed in.");}
    this.id = id; // the id of the collection node
    this.spanIdentifier = spanIdentifier; // the span that visualizes the linkage, if applicable
    this.attrName = attrName;
    this.isMultiSelectable = isMultiSelectable;
    this.linkages = {};
}

p2.LinkageVertex.prototype.hasLinkInfo = function(dataNodeId){
    return this.linkages[dataNodeId] == null ? false : true;
}

p2.LinkageVertex.prototype.link = function(dataNodeId){
    if (dataNodeId === undefined){debugger; throw Error("dataNodeId must not be undefined.")};
    if (!this.isMultiSelectable){
        for (var id in this.linkages){
            if (!id) debugger;
            this.linkages[id] = false;
        }
    }
    if (dataNodeId != null){
        this.linkages[dataNodeId] = true;
        p2.datashackle.core.session.graph.insertEdge(this.id, dataNodeId);
    }
}

p2.LinkageVertex.prototype.unlink = function(dataNodeId){
    if (dataNodeId === undefined){debugger; throw Error("dataNodeId must not be undefined.")};
    if (this.id == dataNodeId){debugger; throw Error("Link collection and target dataNodeId are identical.")}
    this.linkages[dataNodeId] = false;
    p2.datashackle.core.session.graph.insertEdge(this.id, dataNodeId);
}

p2.LinkageVertex.prototype.isLinked = function(dataNodeId){
    if (dataNodeId === undefined){debugger; throw Error("dataNodeId must not be undefined.")};
    if (this.linkages[dataNodeId] == null){debugger; throw Error("No linkage information for dataNodeId " + dataNodeId)};
    return this.linkages[dataNodeId];
}

p2.Setobject = function(module, type, id, action) {
    if (action === undefined) {debugger; throw new Error("Action can't be undefined.");}
    this.action = action;
    this.id = id;
    this.type = type;
    this.module = module;
    this.attrs = {};
}

p2.Setobject.prototype.setAction = function(action){
    this.action = action;
}

p2.Setobject.prototype.setAttr = function(attr_name, value, spanIdentifier){
    this.attrs[attr_name] = new p2.Attribute(attr_name, value, spanIdentifier);
}

p2.Setobject.prototype.getAttr = function(attr_name){
    try {
        return this.attrs[attr_name].value;
    }catch(err){
        debugger;
    }
}

p2.Setobject.prototype.offerSetAttr = function(attr_name, value, spanIdentifier){
    // attribute value is only set if it doesn't exist yet.
    if (this.attrs[attr_name] == undefined){
        this.setAttr(attr_name, value, spanIdentifier);
    }else{
        // Attribute value is already in graph.
        // It has precedence over the offered value.
        // Return it instead.
        value = this.attrs[attr_name].value;
    }
    return value;
}

