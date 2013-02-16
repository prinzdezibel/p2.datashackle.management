// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.datashackle.core");

p2.datashackle.core.Session = function(){
    this.graph = new p2.SetobjectGraph();
}

p2.datashackle.core.buildChangeEventName = function(type, id, attrName){
    // replace dotted names with "_" because the events type property seems to be truncated if dotted names are used.
    return 'mapchange_' + id + '_' + type + '_' + attrName;
}

p2.datashackle.core.triggerChangeOnElement = function(domElement) {
    //Mark a specific setobject as changed. domElement: a reference the html dom node (the input element) of the setobject
    $(document).trigger("global-mark-dirty");
    var dataid = $(domElement).closest('.p2-form').attr('data-node-id');
    $(document).trigger("form-mark-dirty", dataid);
}

p2.datashackle.core.handleChangeEvent = function(element, setobject, dataType, attr_name, spanIdentifier){
   var eventName = p2.datashackle.core.buildChangeEventName(setobject.type, setobject.id, attr_name);
   
   // change event binding
   $(element).bind('blur change keydown keyup', function(e){
       if (dataType == 'checkbox'){
           //var value = $(element).is(':checked') ? 1 : null; // Little hack to make the checkbox datatype work with
                                                             // String and Boolean database fields. In designer mode
                                                             // the checkbox state is saved as string in "span_value".
            var value = $(element).is(':checked') ? 1 : 0;
       }else{
           var value = $(element).val();
       }
       var oldvalue = setobject.getAttr(attr_name);
       setobject.setAttr(attr_name, value, spanIdentifier);
       if (oldvalue != value) {
           p2.datashackle.core.triggerChangeOnElement(element);
       }
       $(document).trigger(eventName, [element, value]);
       return true;
   });

   $(document).bind(eventName, function(e, senderEl, value){
       if (element != senderEl){
           $(element).val(value);
       }
   });
};

p2.datashackle.core.Session.prototype.lookupDataNode = function(dataNodeId){
    var adjlist = this.graph.queryGraphObject(dataNodeId);
    if (adjlist == false){
        throw new Error("Graph node not found.");
    }
    return adjlist.vertex;
}

p2.datashackle.core.Session.prototype.registerDataNode = function(type, id, action){
    if (action === undefined){debugger; throw Error("Parameter 'action' must not be undefined.")}
    var adjlist = this.graph.queryGraphObject(id);
    if (adjlist == false){
        var setobject = new p2.Setobject(type, id, action);
        adjlist = this.graph.insertVertex(setobject);
    }
    if (adjlist.vertex.action != 'delete') {
        //don't override a local delete action
        adjlist.vertex.setAction(action);
    }
    return adjlist.vertex;
}

p2.datashackle.core.Session.prototype.deleteNode = function(setobjectId) {
    node = this.graph.queryGraphObject(setobjectId);
    if (node == false) {
        throw new Error("Vertex " + setobjectId + " cannot get deleted since it doesn't exist");
    }
    this.graph.deleteGraphObject(setobjectId);
}


p2.datashackle.core.Session.prototype.registerLinkageNode = function(sourceId, linkageId, attrName, isMultiSelectable, spanIdentifier){
    if (!linkageId) return;
    if (isMultiSelectable == null){debugger; throw Error("isMultiSelectable must be passed in.");}

    var adjlist = this.graph.queryGraphObject(linkageId);
    if (adjlist === false){
        var linkageVertex = new p2.LinkageVertex(linkageId, attrName, isMultiSelectable, spanIdentifier);
        adjlist = this.graph.insertVertex(linkageVertex);  
        this.graph.insertEdge(sourceId, adjlist.vertex.id);
    }
    return adjlist.vertex;
}

p2.datashackle.core.Session.prototype.commitToServer = function(saveView){
    var self = this;
    var xml = this.graph.toXml(null);
    var success = false;
    var errorshown = false;
    alert(xml);
    $.ajax({url: saveView,
        async: false,
        dataType: "json",
        type: "POST",
        data: {'graph': xml},
        success: function(data, textStatus, xmlHttpRequest){
            if (data.error !== undefined){
                errorshown = true;
                self.displayOverlay(350, 250, data.error);
            }else{
                success = true;
            }
        }
    });
    if (errorshown == false && success == false) {
        var error = new Object();
        error.title = "Cannot save";
        error.message = "Save failed due to error during network request";
        self.displayOverlay(350, 250, error);
    }
    return success;
}


p2.datashackle.core.Session.prototype._xhrComplete = function(result){
    xmlHttpRequest = result[0];
    code = result[1];
	if (code != 'success'){
		alert("Error while saving: (" + xmlHttpRequest.responseText + ")");
	}else{
	    alert(xmlHttpRequest.responseText);
	}
}

p2.datashackle.core.Session.prototype.displayOverlay = function(width, height, error){
	var $msg = $('<div><p>' + error.message + '</p></div>');
    var options = {
		autoOpen: true,
		height: height,
		width: width,
		modal: true,
		open: null,
		title: error.title,
		buttons: {
			'OK': function(){
                $msg.dialog('close');
                // Highlight markup element, if given
                if (error.data_node_id != null){
                    var $elem = $('[data-node-id="' + error.data_node_id + '"]');
                    var $input = $elem.children('.input');
                    $input.effect("highlight", {}, 3000);
                }
            }
		},
	};
	// show dialog
    $msg.dialog(options);
}
p2.datashackle.core.Session.prototype.outputGraph = function(vertexid) {
    var rootvertex = undefined;
    if (vertexid != undefined) {
        rootvertex = this.graph.findRootVertex(vertexid);
    }
    alert(this.graph.toXml(rootvertex));
}

// global Session
p2.datashackle.core.session = new p2.datashackle.core.Session(); 

// global Exception handler
window.onerror = function(errorMsg, url, line){
    alert("Error at " + url + " (" + line  + "): " + errorMsg);
    return false; //this gets us backtrace/other debugging helpers in Firebug (will make it an 'uncaught error')
};

