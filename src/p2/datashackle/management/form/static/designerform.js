// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");


p2.ListlayoutForm = function(dataNodeId, parentEl){
    var url = 'configuration/meta/p2_form/forms/manage_flow_formlayout';
    p2.Formloader.call(this, url, 'OPERATIONAL', sourceId=null, dataNodeId, parentEl);
};

p2.ListlayoutForm.prototype = function(){
	function instance(){};
	instance.prototype = p2.Formloader.prototype;
	return new instance();
}();

p2.ListlayoutForm.prototype.constructor = p2.ListlayoutForm;


p2.DesignerForm = function(module,
                           type,
                           parentEl,
                           plan_identifier,
                           plan_url,
                           windowId,
                           windowTitle,
                           schemeHostPath,
                           operational,
                           dataNodeId,
                           soModule,
                           soType,
                           action,
                           collectionId,
                           applicationUrl
                           ){
    var self = this;
    this.schemeHostPath = schemeHostPath;
    this.plan_identifier = plan_identifier;
    this.plan_url = plan_url;
    this.viewSave = '@@committoserver';
    this.module = module;
    this.type = type;
    this.windowTitle = windowTitle;
    this.operational = operational;
    this.soModule = soModule;
    this.soType = soType;
    this.dataNodeId = dataNodeId;
    this.action = action;
    // collection_id of the form's widget collection
    this.collectionId = collectionId;
    this.applicationUrl = applicationUrl;

    var defaults = {windowTitle: windowTitle,
                    windowId: windowId,
                    resizeable: true,
                    resizeCallback: function(){self.setDirty();$(document).trigger('global-mark-dirty');},
                    maximizeButton: false,
                    closeButton : false,
                    minimizeButton: false,
                    close: function(){
                        self._onClose(formName);
                    }
                    };
    var dataNode = p2.datashackle.core.session.registerDataNode(this.module, this.type, this.dataNodeId, this.action);
    p2.datashackle.core.session.registerLinkageNode(this.dataNodeId, this.collectionId, 'widgets', isMultiSelectable=true);
    
    var openFn = function(){
            var args = Array.prototype.slice.call(arguments, 0);
            args = args.concat([function(){p2.DesignerForm.prototype.opened.apply(self, arguments)}]);
            p2.Formloader.prototype.open.apply(self, args)};

    p2.Formloader.call(this, schemeHostPath, 'DESIGNER', sourceId=null, dataNodeId);
    p2.Window.call(this, parentEl, windowId, openFn, defaults);
  
/* Property form for form windows *//* 
    var propertyform = new p2.PropertyForm(
        this.applicationUrl + '/configuration/meta/p2_form/forms/form_properties', 
        sourceId=null, 
        dataNodeId
    );
    $(this.rootEl).children('div.window-titleBar').click(function(){
        propertyform.open();
    });    
*/
}

p2.DesignerForm.prototype.initNode = function(node) {
    node.setAttr('so_type', this.soType);
    node.setAttr('so_module', this.soModule);
}

p2.DesignerForm.prototype.opened = function(element){
    var self = this;
    var dataNode = p2.datashackle.core.session.registerDataNode(this.module, this.type, this.dataNodeId, this.action);
    this.initNode(dataNode);
     // register for window size changes
     $(this.rootEl).bind('MSG_WINDOW_SIZE_CHANGED', function(e, width, height){
         var form = $(self.rootEl).find('.p2-form');
         form.css({
            width: width + 'px',
            height: height + 'px'
         });
         dataNode.setAttr('css', $(form).attr('style'));
     });
}


p2.DesignerForm.prototype.onSave = function(){
    p2.datashackle.core.session.commitToServer(this.plan_url + '/' + this.viewSave, function(){self.reloadGraph();});
}

p2.DesignerForm.prototype.setDirty = function(){
    $(this.formEl).attr('data-action', 'save');
}

applyInheritance(p2.DesignerForm, p2.Window, p2.Formloader);
