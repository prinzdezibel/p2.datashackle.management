// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Span.Fileupload");

p2.Span.Fileupload = function(el, sourceId, applicationUrl, info){
    var self = this;
    this.info = info;
    this.rootEl = el;
    this.sourceId = sourceId;
    this.applicationUrl = applicationUrl;
    
    // $(el).attr('style', info.css);
    $(el).attr('data-span-type', info.span_type);
    
    var uploadField = $(el).find('input[type="file"]');
    if (info.operational && !info.archetype){
        // Register the linkage node for the media object
        var collectionNode = p2.datashackle.core.session.registerLinkageNode(info.data_node_id, info.collection_id, info.attr_name, isMultiSelectable=false, info.span_identifier);

        this.thumbnail = $(el).find('.thumbnailcontent');

        $(el).find('.cabinet').bind('mousemove', function(e){
	    		var offset = $(this).offset();
	    		var x = e.pageX - offset.left;
	    		var y = e.pageY - offset.top;
	    		var w = $(uploadField).width();
                
	    		$(uploadField).css('top', y - 1 + 'px');
	    		$(uploadField).css('left', x - w + 1 + 'px');
        });

            uploadField.html5_upload({
                url: function(number) {
                    var url = applicationUrl + '/@@upload';
                    return url;
                },
                sendBoundary: window.FormData || $.browser.mozilla,
                setName: function(text) {
                    // self.fileName = text;
                    //$('#progress_report_name').text(text);
                },
                setStatus: function(text) {
                       // $('#progress_report_status').text(text);
                },
                setProgress: function(val) {
                        //self.progressbar.css('width', Math.ceil(val*100)+'%');
                },
                onStartOne: function(event, xhr, name, number, total){
                    var thumbnailWidth = $(this).parents('.p2-span').width();
                    xhr.setRequestHeader("X-thumbnail-width", thumbnailWidth);
                    var thumbnailHeight= $(this).parents('.p2-span').height();
                    xhr.setRequestHeader("X-thumbnail-height", thumbnailHeight);
                    return true; 
                },
                onFinishOne: function(event, response, name, number, total) {
                    // $('#progress_report_bar').hide();
                    var response = $.parseJSON(response);
                    if (response.error){
                        alert('Error: ' + response.error.message);
                    }else{
                        var result = response.result;
                        
                        // Register the media node
                        var media = p2.datashackle.core.session.registerDataNode("p2.datashackle.core.models.media", "Media", result.id, 'save');
                        // And link it.
                        var linkageVertex = p2.datashackle.core.session.graph.lookupGraphObject(collectionNode.id).vertex;
                        linkageVertex.link(result.id);
                                            
                        if (result.has_thumbnail){
                             self.displayThumbnail(result.id, result.file_name);
                        }
                    }
                }
            });

            if (info.media_id != null){
                // Register the media node
                var media = p2.datashackle.core.session.registerDataNode("p2.datashackle.core.models.media", "Media", info.media_id, 'save');
                // And link it.
                collectionNode.link(info.media_id);

                // set thumbnail if applicable
                if (info.has_thumbnail){
                    this.displayThumbnail(info.media_id, info.file_name);
                }
            }   
    }
    if (info.archetype || !info.operational) {
        // Bind a no-op to the input field
        uploadField.click(function(){return false;});
    }
    if (!info.operational && !info.archetype) {

        // resizable button handler
	    $(el).find('.resizable').each(function(){
	        $(this).target = el;
	        $(this).css('top', '100%');
	        $(this).mousedown(function(ev){
	            self.resizableMousedown(ev);
	            return false;
	        });
	    });
        this.registerDataNode();
    }
}


p2.Span.Fileupload.prototype = function(){
    function instance(){};
	instance.prototype = p2.Span.prototype;
	var obj = new instance();
    return obj;
}();

p2.Span.Fileupload.prototype.constructor = p2.Span;


p2.Span.Fileupload.prototype.displayThumbnail = function(media_id, fileName){
    // this.progressbar.hide();
    var imageUrl = this.applicationUrl + '/@@media?id=' + media_id;
    var thumbnailUrl = imageUrl + '&thumbnail'; 
    var anchor = $('<a target="_blank">');
    anchor.attr('title', fileName);
    anchor.attr('href', imageUrl);
    var img = $('<img>');
    img.attr('src', thumbnailUrl);
    // img.attr('load', function(){});
    $(this.rootEl).find('.container').html(img);
}



