// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");



p2.Formloader = function(url, mode, sourceId, setobjectId, parentEl){
    if (mode != 'OPERATIONAL' && mode != 'DESIGNER') throw Error("Mode MUST have one of the values 'OPERATIONAL', 'DESIGNER'");
    if (sourceId === undefined) throw Error("sourceId is mandatory, although it could be null.");
    if (setobjectId === undefined) throw Error("setobjectId is mandatory, although it could be null.");
    this.url = url;
    this.formEl = null;
    this.mode = mode;
    this.sourceId = sourceId;
    this.setobjectId = setobjectId;
    this.parentEl = parentEl;
}

p2.Formloader.prototype.load = function(success){
    var self = this;
    var data = {};
    data.mode = this.mode;
    data.show_strip = false;
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
    $.ajax({url: this.url,
        data: data,
        async: true,
        type: 'POST',
        timeout: 20000, //20 seconds
        success: function(contentHtml, textStatus, xhr){
            // Insert form to DOM
            $(self.parentEl).append(contentHtml);
            self.formEl = $(self.parentEl).children('.p2-form');
            $(self.formEl).bind('widget_change', function(e){
                self.setDirty();
            });
            // issue the callback
            if (success){
                success(self.formEl, self);
            }
        }
    });
    
}

p2.Formloader.prototype.open = function(parentEl, success) {
    this.parentEl = parentEl;
    return this.load(success);
}


