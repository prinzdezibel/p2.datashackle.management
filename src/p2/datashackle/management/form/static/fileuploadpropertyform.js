// Copyright (C) projekt-und-partner.com, 2011
// Author:  Jonas Thiem <jonas.thiem%40projekt-und-partner.com>

namespace("p2");

p2.FileuploadPropertyform = function(propertyformSchemeHostPath, propertyFormSourceId, propertyformSetobjectId) {
    p2.PropertyForm.call(this, propertyformSchemeHostPath, propertyFormSourceId, propertyformSetobjectId);
}

p2.FileuploadPropertyform.prototype = function() {
    function instance(){};
	instance.prototype = p2.PropertyForm.prototype;
	return new instance();
}();

p2.FileuploadPropertyform.prototype.constructor = p2.PropertyForm;

p2.FileuploadPropertyform.prototype.open = function() {
    // If dialog is already there, we don't load it again from database
    if (!this.isLoaded){
        var self = this;
        p2.Formloader.prototype.open.call(this, this.rootEl, function(){self.isLoaded = true; self.initialize();}, this.sourceId);
    }
	$(this.dialog).dialog('open');
}


p2.FileuploadPropertyform.prototype.initialize = function() {
    var widget = this.getmappinginput();
    var self = this;
    self.mappingvalue = this.getmappinginput().val();
    if (widget.length) {
        var func = function(e) {self.mappingnamechanged();};
        //widget.bind('change', func);
        widget.bind('keydown', func);
        widget.bind('keyup', func);
        widget.bind('blur', func);
    }
    this.getmappinginput().focus();
    //add some fields manually to the setobject (we don't allow the user to influence/set this since that would be pointless)
    setobjectid = this.getmappinginput().parent().parent().attr('data-node-id');
    formsetobject = p2.setdesigner.findParentFormVertex(setobjectid);
    setobject = p2.datashackle.core.session.graph.queryGraphObject(setobjectid);
    
    if (!formsetobject) {
        alert("fileuploadpropertyform.js: form node not found");return;
    }
    if (setobject) {
        setobject.vertex.setAttr('source_module', formsetobject.getAttr("so_module"));
        setobject.vertex.setAttr('source_classname', formsetobject.getAttr("so_type"));
        setobject.vertex.setAttr('target_module', 'p2.datashackle.core.models.media');
        setobject.vertex.setAttr('target_classname', 'Media');
    }else{
        alert("fileuploadpropertyform.js: setobject node not found...");
    }
}

p2.FileuploadPropertyform.prototype.getforeignkeyinput = function() {
    return $(this.rootEl).find('div[data-field-identifier="foreignkeycol"] > .input');
}

p2.FileuploadPropertyform.prototype.getmappinginput = function() {
    return $(this.rootEl).find('div[data-field-identifier="attr_name"] > .input');
}

p2.FileuploadPropertyform.prototype.setwidgetvalue = function(widget, newvalue) {
    widget().val(newvalue);
}

p2.FileuploadPropertyform.prototype.mappingnamechanged = function() {
    var newmappingvalue = this.getmappinginput().val();
    if (newmappingvalue == self.mappingvalue) {return;}
    self.mappingvalue = newmappingvalue;
    
    var newvalue = "fk_" + newmappingvalue;
    this.getforeignkeyinput().val(newvalue);
    this.getforeignkeyinput().trigger('blur');
}


