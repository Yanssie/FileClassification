const pool = require('../models/db');

function show(res, req) {
	query = "select features.name as name, features.cluster as cluster from features;"
    pool.query(query, function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
        	var cluster1 = [];
        	var cluster2 = [];
        	var cluster3 = [];
        	for(i = 0; i < result.rows.length; i++) {
        		if (result.rows[i].cluster == 0) {
        			cluster1.push(result.rows[i].name);
        		} else if(result.rows[i].cluster == 1) {
        			cluster2.push(result.rows[i].name);
        		} else if(result.rows[i].cluster == 2) {
        			cluster3.push(result.rows[i].name);
        		}
        	}
        	res.render('cluster.jade', {
        		title: "Cluster Results",
        		cluster1: cluster1,
        		cluster2: cluster2,
        		cluster3: cluster3
        	});
        }

    });

}

function get_json(res, req) {
    var val = req.query.name;
    console.log(val);
    query = "select data from jsonstore where name='" + val + "';"
    pool.query(query, function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
            var data = JSON.stringify(result.rows[0].data);
            res.send(data);
        }

    });


}


exports.do_work = function(req, res) {
	show(res, req);
}

exports.ajax_work = function(req, res) {
    get_json(res, req);
}