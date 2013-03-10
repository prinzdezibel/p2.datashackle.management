// Copyright (C) projekt-und-partner.com, 2011
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Span.Action");

p2.Span.Action = function(el, sourceId, info, actionurl){
    var self = this;

    this.info = info;
    this.actionurl = actionurl;
    this.rootEl = el;
    this.sourceId = sourceId;
       
   
   	if (info.operational == false){
        this.registerDataNode();
    }
    
    //var click = function(event){
    //    debugger;
    //    if (self.info.submit){
    //        var form = $(el).parents('.p2-form');
    //        var nodeId = $(form).attr('data-node-id');
    //        var inputName = 'form_' + $(form).attr('data-form-identifier');
    //        inputName += '.action.';
    //        inputName += self.info.aktion;
    //        var sess = p2.datashackle.core.session;
    //        //var graph = sess.graph.queryGraphObject(nodeId);
    //        var data = sess.graph.toXml(nodeId);
    //        if (self.info.ajax){
    //            // var xml = this.graph.toXml(null);
    //            alert(data);
    //            var data = {data: data};
    //            data[inputName] = '1';
    //            $.ajax({url: self.actionurl,
    //                    async: false,
    //                    dataType: "json",
    //                    type: self.info.method,
    //                    data: data,
    //                    success: function(data, textStatus, xmlHttpRequest){
    //                        if (data.error !== undefined){
    //                            errorshown = true;
    //                            alert(data.error);
    //                        }else{
    //                            success = true;
    //                        }
    //                    },
    //                    error: function(xhr, text, error){
    //                        alert(error);
    //                    }
    //            });
    //        }else{
    //            var form = $('<form style="display: none"' +
    //                         ' action="' + self.actionurl + '"' +
    //                         ' method="' + self.info.method + '">');
    //            var textarea = $('<textarea name="data"/>')
    //            textarea.text(data);
    //            form.append(textarea);
    //            var submit = $('<input type="text" name="' + inputName +
    //                           '" value="1"/>');
    //            form.append(submit);
    //            var planIdNode = $('<input type="text" name="plan_identifier" value="' +
    //                            planId + '" />');
    //            form.append(planIdNode);
    //            var tableNode = $('<input type="text" name="table_identifier" value="' +
    //                            tableId + '" />');
    //            form.append(tableNode);
    //            $('body').append(form);
    //            form.submit(); 
    //        }
    //    }
    //    if (self.info.msg_reset){
    //        $(el).trigger('P2_RESET', []);
    //    }
    //    if (self.info.msg_close){
    //        $(el).trigger('P2_CLOSE', []);
    //    }
    //}

    // $(el).bind('click', click);
}

p2.Span.Action.prototype = function(){
    function instance(){};
	instance.prototype = p2.Span.prototype;
	var obj = new instance();
    return obj;
}();

p2.Span.Action.prototype.constructor = p2.Span;


