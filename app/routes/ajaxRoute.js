const pool = require('../models/db');
var d3 = require("d3");

exports.get_xml = function(req, res) {
    get_original(res, req);
}

exports.get_json = function(req, res) {
    get_apg(res, req);
}

exports.get_feature = function(req, res) {
    get_cluster(res, req);
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

function get_cluster(res, req) {

    query = "select name, cluster from features;"
    pool.query(query, function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
            var names = result.rows[0].name;
            var cluster = result.rows[0].cluster;

            // update(nodes);
            res.send(names, cluster);
        }

    });

}
