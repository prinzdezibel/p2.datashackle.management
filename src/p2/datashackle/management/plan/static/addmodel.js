$(document).ready(function(){
    $('#add_model_view\\.action\\.add').click(function(){
        var form = $(this).parents('.p2-form');
        var nodeId = $(form).attr('data-node-id');
        var sess = p2.datashackle.core.session;
        var data = sess.graph.toXml(nodeId);
        var vertex = p2.datashackle.core.session.graph.queryGraphObject(nodeId);
        var planId = vertex.vertex.getAttr('plan_identifier');
        var tableId = vertex.vertex.getAttr('table');
        var klass = vertex.vertex.getAttr('klass');
        var form = $('<form style="display: none"' +
                     ' action="' + window.location.href + '"' +
                     ' method="POST">');
        var textarea = $('<textarea name="data"/>')
        textarea.text(data);
        form.append(textarea);
        var submit = $('<input type="text" name="' + $(this).attr('name') +
                       '" value="' + $(this).text() + '"/>');
        form.append(submit);
        var planIdNode = $('<input type="text" name="plan_identifier" value="' +
                        planId + '" />');
        form.append(planIdNode);
        var tableNode = $('<input type="text" name="table_identifier" value="' +
                        tableId + '" />');
        form.append(tableNode);
        var klassNode = $('<input type="text" name="klass" value="' +
                        klass + '" />');
        form.append(klassNode);
        $('body').append(form);
        form.submit(); 
    });
});
