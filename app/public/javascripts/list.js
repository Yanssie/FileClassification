$body = $("body");

$(document).ready(function(){
    $('.cluster-btn').on("click", function(){
        $body.addClass("loading");
    });

    $('.xml-link').on('click', function () {

    	var params = { name: $(this).attr('name') };

        //ajax call defined in app 
    	$.get( '/ajax_get_xml',params, function(data) {
    		$('.xmlcontent').html(data);
    	});
        $('.xmlcontent').show();
        $('.jsoncontent').hide();

    });

    $('.xml-button').on('click', function () {

        var params = { name: $(this).attr('name') };

        //ajax call defined in app 
        $.get( '/ajax_get_xml',params, function(data) {
            $('.xmlcontent').html(data);
        });
        $('.xmlcontent').show();
        $('.jsoncontent').hide();
    });

    $('.json-link').on('click', function () {

        var params = { name: $(this).attr('name') };

        //ajax call defined in app 
        $.get( '/ajax_get_json',params, function(data) {
            $('.jsoncontent').html(data);
        });
        $('.xmlcontent').hide();
        $('.jsoncontent').show();
    });

    $('.json-button').on('click', function () {

        var params = { name: $(this).attr('name') };

        //ajax call defined in app 
        $.get( '/ajax_get_json',params, function(data) {
            $('.jsoncontent').html(data);
        });
        $('.xmlcontent').hide();
        $('.jsoncontent').show();
    });

})
