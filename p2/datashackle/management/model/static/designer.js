// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");

p2.Setdesigner = function(applicationUrl, plan_url, plan_identifier, table_identifier, formType)
{
    this.plan_identifier = plan_identifier;
    this.table_identifier = table_identifier;
    this.plan_url = plan_url;
    this.applicationUrl = applicationUrl;
    this.formType = formType;
    this.listlayoutForms = {};
    
    var rootEl = $('#view_area');
    var self = this;
	var options = {};
	// call superclass constructor
	p2.WindowManager.call(this, plan_identifier, rootEl, options);

	// set up bin packer for arranging windows in a way
	// they don't overlap.
	var windowPadding = {
		top: 35,
		right: 15,
		bottom: 35,
		left: 15
	};
	
	// Bind formreset event
	$(this.rootEl).bind('formreset', function(ev, form_name, windowTitle, url, width, height){
	    var form = ev.target;
        $(form).remove();
        self.fetch_form(form_name, windowTitle, url);
	});
    
    // Bind to window size changed event 
    $(this.rootEl).bind('MSG_WINDOW_SIZE_CHANGED', function(e, width, height){
        
        self.setSiteSize({height:height, width:width});
    });
	
	var availableWidth = $('#dolmen-site').width() - $('#toolbox').width();
	
	var self = this;
}

p2.Setdesigner.prototype = function(){
	function instance(){};
	instance.prototype = p2.WindowManager.prototype;
	return new instance();
}();

p2.Setdesigner.prototype.constructor = p2.Setdesigner;

p2.Setdesigner.dropWidget = function(event, ui, window)
{	// **this** refers to the setdesigner window manager instance.
	// window parameter refers to the (p2-)window object being dropped onto.
	if (ui.helper.parents().is("#composites")){
		var archetypeId = ui.helper.attr('id');
		var formEl = $(window.formEl);
		var sourceId = $(window.formEl).attr('data-linkage-node-id');
		p2.Widget.appendNew(formEl, ui.helper, window);
	}
}

p2.Setdesigner.resizeOrigin = {clientX: 0, clientY: 0};
p2.Setdesigner.resizeElement = null;
p2.Setdesigner.resizeMove = false;

p2.Setdesigner.resizableMousedown = function(ev)
{
	p2.Setdesigner.resizeOrigin = {clientX : ev.clientX, clientY : ev.clientY};
	p2.Setdesigner.resizeMove = true;
	if ($(this).parent().is('#dialog_view')){
		p2.Setdesigner.resizeElement = $('#dialog_view');
		$('#dolmen-site').data('original-height', $('#dolmen-site').outerHeight(true))
	}else{
		// for input elements, the affected control is the previous sibling.
		p2.Setdesigner.resizeElement = $(this).prev();
	}
	//stop both default action and event bubbling
	return false;
};

p2.Setdesigner.stopSelection = function(event)
{
	// mark all children of an ui-selected widget as selected
	var windowContent = this;
	$(windowContent).find('.ui-selected').parents('.p2-widget').find('*').each(function(){
		$(this).addClass('ui-selected');
	})
}

p2.Setdesigner.prototype.newForm = function(formName){
     var url = p2.setdesigner.plan_url + '/forms/' + formName + '/@@baseform';
     return p2.setdesigner.fetch_form(formName, formName, url);
}

p2.Setdesigner.prototype.fetch_form = function(
        form_name,
        windowTitle,
        url,
        dataNodeId,
        klass,
        action,
        collectionId
        ){
    var parentEl = $(this.rootEl).find('.windows-screen-estate');
    var form = new p2.DesignerForm(this.formType,
                                    parentEl,
                                    this.plan_identifier,
                                    this.plan_url,
                                    form_name,
                                    windowTitle,
                                    url,
                                    operational = false,
                                    dataNodeId,
                                    klass,
                                    action,
                                    collectionId,
                                    this.applicationUrl
                                    );
	this._append_window(form_name, form);
   
    $('#' + $(form.formEl).attr('data-form-identifier') + '\\.action\\.save').click(function(){
       debugger; 
       var form = $(this).parents('.p2-form');
       var nodeId = $(form).attr('data-node-id');
       var sess = p2.datashackle.core.session;
       var xml = sess.graph.toXml(nodeId);
       //var form = $('<form style="display: none"' +
       //             ' action="' + url + '"' +
       //             ' method="POST">');
       //var textarea = $('<textarea name="data"/>')
       //textarea.text(data);
       //form.append(textarea);
       //var submit = $('<input type="text" name="' + $(this).attr('name') +
       //                '" value="' + $(this).text() + '"/>');
       //form.append(submit);
       //$('body').append(form);
       //form.submit(); 
       var data = {};
       data['data'] = xml;
       data[$(this).attr('name')] = $(this).text();
               $.ajax({url: url,
                       async: false,
                       dataType: "json",
                       type: "POST",
                       data: data,
                       success: function(data, textStatus, xmlHttpRequest){
                           if (data.error !== undefined){
                               errorshown = true;
                               alert(data.error);
                           }else{
                               success = true;
                           }
                       },
                       error: function(xhr, text, error){
                           alert(error);
                       }
               });
    });

	return form;
}

p2.Setdesigner.prototype.showForm = function(el, form_id){
    // clear active item
    $(el).parents('.forms').find('.active').each(function(){
    $(this).removeClass('active')});
    for (var i = 0; i < this.windows.length; i++){
        var window = this.windows[i];
        if (window.dataNodeId == form_id){
            window.fadeIn();
            $(el).parent().addClass('active');
        }else{
            window.fadeOut();
        }
    }
}

p2.Setdesigner.prototype.setSiteSize = function(size){
      var formHeight = size.height;
      var toolbarFudgePixels = 2 * 25; // correlates to dolmen-inner-body margin
      var formFudgePixels = 2 * 25 + 50; // depends on dolmen-inner-body AND window decorator shape
      var toolboxHeight = $('#toolbox').outerHeight(true) + toolbarFudgePixels;
      var navHeight = $('#effect').outerHeight(true);
      if ((formHeight + formFudgePixels) > toolboxHeight && (formHeight + formFudgePixels) > navHeight){
          $('#dolmen-site').height(formHeight + formFudgePixels);
      }else if (toolboxHeight > navHeight){
          $('#dolmen-site').height(toolboxHeight);
      }else{
          $('#dolmen-site').height(navHeight);
      }

    var formWidth = size.width;
    var toolbarWidth = $('#toolbox').outerWidth(true);
    var siteWidth = formWidth;
    $('#dolmen-inner-body').width(siteWidth);   
 
}

// Append window to DOM and intialise window
p2.Setdesigner.prototype._append_window = function(formName, window){
    var self = this;
	var windowAndButton = p2.WindowManager.prototype.registerWindow.call(self, formName, window);	

    // $(window.rootEl).selectable({
    //  stop : p2.Setdesigner.stopSelection
    // });
		
	$(window.rootEl).droppable({
        accept: '.p2-widget, .window-container, .assoc-window-container, li',
	    drop:  function(event, ui){
			ui.helper.removeClass('over-droppable');
			// Extend the "arguments object" that is not a native array
			// even if it seems at the first glance to be so.
			var args = Array.prototype.slice.apply(arguments);
			args = args.concat(new Array(window));
			if (ui.helper.hasClass('p2-widget')){
				return p2.Setdesigner.dropWidget.apply(self, args);	
			}else{
				// assoc-window-container
				// do nothing.
			}
		},
		over: function(event, ui){
			//ui.helper.addClass('over-droppable');
		},
		out: function(event, ui){
			//ui.helper.removeClass('over-droppable');
		}
	});
	
}


p2.Setdesigner.fetchArchetypeHelper = function(ev){
	var $archetype = $(ev.currentTarget).find('.window-container');
	var $window = $archetype.clone();
	$window.data('window', $archetype.data('window'));
	$window.show();	
	return $window.get(0);
}

p2.Setdesigner.prototype.initializeArchetype = function(window){
	// **this** refers to the setdesigner window manager instance.
	
    var listItem = $(window.rootEl).parents('.draggable');
	$(listItem).draggable({
			revert : 'invalid',
			helper : function(){
				return p2.Setdesigner.fetchArchetypeHelper.apply(self, arguments);
			},
			scroll : false,
			zIndex : 1000,
			appendTo : '.windows-screen-estate',
			revertDuration : 400,
			cursor : 'move',
			delay  : 300,
	});
}

p2.Setdesigner.prototype.findParentFormVertex = function(vertexId){
    var go = p2.datashackle.core.session.graph.queryGraphObject(vertexId);
    if (go == false) throw new Error("Vertex " + vertexId + " does not exist in graph (findParentFormNode).");
    
    do {
        do {
            if (go.parent == null) {return undefined;}
            go = go.parent;
        } while (!go.vertex instanceof p2.Setobject)
    } while (go.vertex.type != "FormType")
    return go.vertex;
}

p2.Setdesigner.prototype.reloadPage = function() {
    //lateron, we want to read the current form and add it as a parameter to the reload URL
    $('body').html(''); //wipe out page
    window.location.replace(window.location); //reload
}


p2.Setdesigner.prototype.revert = function() {
    this.reloadPage();
}



p2.Setdesigner.prototype.onFormpropertiesLoaded = function(formId){
      var self = this;
      // bind dropdown selection with form's layout
      $('.p2-span[data-node-id="3429670735"] .input').change(function(){
            if ($(this).val() == 'LIST'){
                // hide all windows
                for (var i = 0; i < self.windows.length; i++){
                    var window = self.windows[i];
                    $(window.rootEl).hide();
                }
                // create new ListlayoutForm, if necessary
                var $form =  $('#listlayoutforms .p2-form[data-node-id="' + formId + '"]');
                if (!$form.length){
                    var form = new p2.ListlayoutForm(formId, $('#listlayoutforms'));
                    form.load();
                    $form = $(form.formEl);
                }
                $form.show();
        
            }else if ($(this).val() == 'FORM'){
                $('#listlayoutforms .p2-form').each(function(){
                   $(this).hide(); 
                });
                self.showForm(null, formId);
            }
      });
}


