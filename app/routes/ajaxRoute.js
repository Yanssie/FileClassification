const pool = require('../models/db');
var d3 = require("d3");

exports.get_xml = function(req, res) {
    get_original(res, req);
}

exports.get_json = function(req, res) {
    get_apg(res, req);
}



function get_original(res, req) {
    var val = req.query.name;
    console.log('response: ' + val);

    query = "select data from xmlstore where name='" + val + "';"
    pool.query(query, function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
            var data = result.rows[0].data;
            res.send(data);
        }

    });
}

function get_apg(res, req) {


    var val = req.query.name;
    console.log(val);
    query = "select data from jsonstore where name='" + val + "';"
    pool.query(query, function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
            var data = result.rows[0].data;
            // update(nodes);
            res.send(data);
        }

    });

}

function update(root) {
    // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse(),
      links = tree.links(nodes);

  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 180; });

  // Declare the nodes…
  var node = svg.selectAll("g.node")
      .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Enter the nodes.
  var nodeEnter = node.enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { 
          return "translate(" + d.y + "," + d.x + ")"; });

  nodeEnter.append("circle")
      .attr("r", 10)
      .style("fill", "#fff");

  nodeEnter.append("text")
      .attr("x", function(d) { 
          return d.children || d._children ? -13 : 13; })
      .attr("dy", ".35em")
      .attr("text-anchor", function(d) { 
          return d.children || d._children ? "end" : "start"; })
      .text(function(d) { return d.name; })
      .style("fill-opacity", 1);

  // Declare the links…
  var link = svg.selectAll("path.link")
      .data(links, function(d) { return d.target.id; });

  // Enter the links.
  link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", diagonal);
}