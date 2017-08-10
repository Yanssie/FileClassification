

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

    // $('.ajax-link').on('click', function () {

    // 	var params = { name: $(this).text() };

    //     //ajax call defined in app 
    // 	$.get( '/ajax_get_json',params, function(data) {

        // ************** Generate the tree diagram  *****************
        // var margin = {top: 20, right: 120, bottom: 20, left: 120},
        // width = 960 - margin.right - margin.left,
        // height = 500 - margin.top - margin.bottom;
    
        // var i = 0;

        // var tree = d3.layout.tree()
        //     .size([height, width]);

        // var diagonal = d3.svg.diagonal()
        //     .projection(function(d) { return [d.y, d.x]; });
  

        // var svg = d3.select(".chart").append("svg")
        //     .attr("width", width + margin.right + margin.left)
        //     .attr("height", height + margin.top + margin.bottom)
        //     .append("g")
        //     .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    // 		$('.jcontent').html(JSON.stringify(data));
    // 	});
    // });

 });