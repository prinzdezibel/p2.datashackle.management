// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");



p2.Formloader = function(schemeHostPath, mode, sourceId, setobjectId){
    if (mode != 'OPERATIONAL' && mode != 'DESIGNER') throw Error("Mode MUST have one of the values 'OPERATIONAL', 'DESIGNER'");
    if (sourceId === undefined) throw Error("sourceId is mandatory, although it could be null.");
    if (setobjectId === undefined) throw Error("setobjectId is mandatory, although it could be null.");
    this.schemeHostPath = schemeHostPath;
    this.formEl = null;
    this.mode = mode;
    this.sourceId = sourceId;
    this.setobjectId = setobjectId;
}

p2.Formloader.prototype.open = function(parentEl, callback) {
    var self = this;
    var data = {};
    data.mode = this.mode;
    data.show_strip = false;
    //compose data with graph and other things:
    if (p2.datashackle.core.session.graph.queryGraphObject(this.setobjectId) != false) {
        var vertex = p2.datashackle.core.session.graph.findRootVertex(this.setobjectId);
        var graph = p2.datashackle.core.session.graph.toXml(vertex.id);
        data.graph = graph;
    }
    if (this.source_id != null){
        data.source_id = this.sourceId;
    }
    if (this.setobjectId != null){
        data.setobject_id = this.setobjectId;
    }
    //fire off request
    $.ajax({url: this.schemeHostPath + '/@@baseform',
        data: data,
        async: true,
        type: 'POST',
        timeout: 20000, //20 seconds
        success: function(contentHtml, textStatus, xhr){
            // Insert form to window container.
            $(parentEl).html(contentHtml);
            self.formEl = $(parentEl).children('.p2-form');
            $(self.formEl).bind('widget_change', function(e){
                self.setDirty();
            });
            // issue the callback
            if (callback){
                callback(self.formEl, self);
            }
            if (this.setobjectId) {
                alert(p2.datashackle.core.session.graph.toXml(this.setobjectId));
            }
        }
    });
}


