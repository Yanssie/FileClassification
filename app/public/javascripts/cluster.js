
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

    $('.btn-secondary').on('click', function() {
      $('.table tr').css('display', 'none').fadeIn('slow');
      var names1 = []; // names of cluster1
      var names2 = [];
      var names3 = [];
      var table = document.getElementsByTagName('table')[0];
      var rows = table.rows;
      for (var i = 0; i < rows.length; i++) {
        var rowText = rows[i].firstChild.textContent;
        if($(rows[i]).attr('data-status') == 'cluster1') {
          names1.push(rowText);
        } else if($(rows[i]).attr('data-status') == 'cluster2') {
          names2.push(rowText);
        } else {
          names3.push(rowText);
        }
      }

      show(names1, names2, names3);
      

    });

    function show(names1, names2, names3) {
      // D3.js Force-directed graph
        var w = window.innerWidth;
        var h = window.innerHeight;
        var svg = d3.select("svg"),
            width = +svg.attr("width"),
            height = +svg.attr("height");
        svg.selectAll("*").remove();

        var color = d3.scaleOrdinal(d3.schemeCategory20);

        var simulation = d3.forceSimulation()
              .force("link", d3.forceLink().id(function(d) { return d.id; }))
              .force("charge", d3.forceManyBody())
              .force("center", d3.forceCenter(width/2, height/2 ));

        // define the json string
        // define the nodes
        var data = '{"nodes": [';
        data += '{"id": "cluster1", "group": 1}, {"id": "cluster2", "group": 2}, {"id": "cluster3", "group": 3},';
        for (i = 0; i < names1.length; i++) {
          if(i == names1.length - 1) {
            data += '{"id": "' + names1[i] + '","group": 1},';
          } else {
            data += '{"id": "' + names1[i] + '","group": 1},';
          }
        }
        for (i = 0; i < names2.length; i++) {
          if(i == names2.length - 1) {
            data += '{"id": "' + names2[i] + '","group": 2},';
          } else {
            data += '{"id": "' + names2[i] + '","group": 2},';
          }
        }
        for (i = 0; i < names3.length; i++) {
          if(i == names3.length - 1) {
            data += '{"id": "' + names3[i] + '","group": 3}';
          } else {
            data += '{"id": "' + names3[i] + '","group": 3},';
          }
        }


        // define the links
        data += '], "links": [';
        for(j = 0; j < names1.length; j ++) {
            data += '{"source": "cluster1", "target": "' + names1[j] + '", "value":' + Math.random()*10  + '},';
        }
        for(j = 0; j < names2.length; j ++) {
            data += '{"source": "cluster2", "target": "' + names2[j] + '", "value":' + Math.random()*10 + '},';
        }
        for(j = 0; j < names3.length; j ++) {
          if(j == names3.length - 1) {
            data += '{"source": "cluster3", "target": "' + names3[j] + '", "value":' + Math.random()*10  + '}';
          } else {
            data += '{"source": "cluster3", "target": "' + names3[j] + '", "value":' + Math.random()*10  +'},';
          }
        }


        data += ']}';

        graph = JSON.parse(data);

console.log(graph.links)
          var link = svg.append("g")
              .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
              .attr("stroke-width", function(d) { return Math.sqrt(d.value); });
console.log(graph.nodes)
          var node = svg.append("g")
              .attr("class", "nodes")
            .selectAll("circle")
            .data(graph.nodes)
            .enter().append("circle")
              .attr("r", 5)
              .attr("fill", function(d) { return color(d.group); })
              .call(d3.drag()
                  .on("start", dragstarted)
                  .on("drag", dragged)
                  .on("end", dragended));

          node.append("title")
              .text(function(d) { return d.id; });

          simulation
              .nodes(graph.nodes)
              .on("tick", ticked);

          simulation.force("link")
              .links(graph.links);

          function ticked() {
          link
              .attr("x1", function(d) { if (d.source.group == 1) return d.source.x - 400;
                                        if (d.source.group == 2) return d.source.x + 1100;
                                        if (d.source.group == 3) return d.source.x + 100; })

              .attr("y1", function(d) { if (d.target.group == 1) return d.source.y - 500; 
                                        if (d.target.group == 2) return d.source.y - 900; 
                                        if (d.target.group == 3) return d.source.y + 800; })

              .attr("x2", function(d) { if (d.source.group == 1) return d.target.x - 400;
                                        if (d.source.group == 2) return d.target.x + 1100;
                                        if (d.source.group == 3) return d.target.x + 100; })

              .attr("y2", function(d) { if (d.target.group == 1) return d.target.y - 500; 
                                        if (d.target.group == 2) return d.target.y - 900; 
                                        if (d.target.group == 3) return d.target.y + 800; });
          node
              .attr("cx", function(d) { if (d.group == 1) return d.x - 400; 
                                        if (d.group == 2) return d.x + 1100 ;
                                        if (d.group == 3) return d.x + 100; })
              .attr("cy", function(d) { if (d.group == 1) return d.y - 500;
                                        if (d.group == 2) return d.y - 900;
                                        if (d.group == 3) return d.y + 800; });
            }

          function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.1).restart();
              d.fx = d.x;
              d.fy = d.y;
            }

          function dragged(d) {
              d.fx = d3.event.x;
              d.fy = d3.event.y;
            }

          function dragended(d) {
            if (!d3.event.active) simulation.alphaTarget(0);
              d.fx = null
              d.fy = null
            }
      }

    // $('.ajax-link').on('click', function () {

    // 	var params = { name: $(this).text() };

    //     //ajax call defined in app 
    // 	$.get( '/ajax_get_json',params, function(data) {


    // 		$('.jcontent').html(JSON.stringify(data));
    // 	});
    // });

 });