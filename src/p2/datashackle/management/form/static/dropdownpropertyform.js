// Copyright (C) projekt-und-partner.com, 2011
// Author:  Jonas Thiem <jonas.thiem%40projekt-und-partner.com>

namespace("p2");

p2.DropdownPropertyform = function(propertyformSchemeHostPath, propertyFormSourceId, propertyformSetobjectId)
{
    p2.PropertyForm.call(this, propertyformSchemeHostPath, propertyFormSourceId, propertyformSetobjectId);
}

p2.DropdownPropertyform.prototype = function()
{
    function instance(){};
	instance.prototype = p2.PropertyForm.prototype;
	return new instance();
}();

p2.DropdownPropertyform.prototype.constructor = p2.PropertyForm;


p2.DropdownPropertyform.prototype.open = function()
{
    // If dialog is already there, we don't load it again from database
    if (!this.isLoaded){
        var self = this;
        p2.Formloader.prototype.open.call(this, this.rootEl, function(){self.isLoaded = true; self.initialize();}, this.sourceId);
    }
	$(this.dialog).dialog('open');
}

p2.DropdownPropertyform.prototype.initialize = function()
{
    //add source table field to the setobject manually (we don't allow the user to influence/set this since that would be pointless)
    setobjectid = this.getforeignkeyinput().parent().parent().attr('data-node-id');
    formsetobject = p2.setdesigner.findParentFormVertex(setobjectid);
    setobject = p2.datashackle.core.session.graph.queryGraphObject(setobjectid);
    if (!formsetobject) {
        alert("dropdownpropertyform.js: form node not found");
        debugger;
        return;
    }
    if (setobject) {
        setobject.vertex.offerSetAttr('target_module', 'p2.datashackle.core.models.setobject_types');
    }else{
        alert("dropdownpropertyfrom.js: setobject node not found");
        debugger;
        return;
    }
}

p2.DropdownPropertyform.prototype.getforeignkeyinput = function()
{
    return $(this.rootEl).find('div[data-field-identifier="foreignkeycol"] > .input');
}

