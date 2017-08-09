
$(document).ready(function () {

    $('.btn-filter').on('click', function () {
      var $target = $(this).data('target');
      if ($target != 'all') {
        $('.table tr').css('display', 'none');
        $('.table tr[data-status="' + $target + '"]').fadeIn('slow');
      } else {
        $('.table tr').css('display', 'none').fadeIn('slow');
      }
    });

    $('.ajax-link').on('click', function () {

    	var params = { name: $(this).text() };

        //ajax call defined in app 
    	$.get( '/ajax_get_json',params, function(data) {
    		$('.jcontent').html(JSON.stringify(data));
    	});
    });

 });