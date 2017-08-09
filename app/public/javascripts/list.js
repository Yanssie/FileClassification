$body = $("body");

$(document).ready(function(){
    $('.cluster-btn').on("click", function(){
        $body.addClass("loading");
    });
})
