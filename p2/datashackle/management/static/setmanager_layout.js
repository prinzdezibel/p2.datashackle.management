namespace("p2.datashackle.core");

$(document).ready(function(){
	$("#togglebar-button").click(function() {
        $("#effect").toggle();
        if ($("#effect").is(':visible')){
		    p2.createCookie('navigation', 'expanded', 1);
    	}else{
	    	p2.createCookie('navigation', 'collapsed', 1);
	    }
		return false;
	});
	
	if (p2.readCookie('navigation') == 'collapsed'){
		$("#effect").toggle();
	}
});
