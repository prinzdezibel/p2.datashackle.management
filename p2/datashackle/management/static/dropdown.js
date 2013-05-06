$(document).ready(function(){
    $("dl.additional-actions").hover(
        function() {
           $("dd", this).show();
           $(this).addClass("unfolding");
        }, 
        function() {
           $("dd", this).hide();
           $(this).removeClass("unfolding");
        } 
    );
});
