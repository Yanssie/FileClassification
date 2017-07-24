const pool = require('../models/db');

//to run a query we just pass it to the pool
//after we're done nothing has to be taken care of
//we don't have to return any client to the pool or close a connection

function get_list(res, req) {
	pool.query('SELECT * from jsonStore', function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
        	output_list(res, req, result.rows);
        }

    });

}

function output_list(res, req, rows) {
    res.render('list_json.jade', {
        		title:"List all the json files",
        		rows: rows
    });
}

exports.do_work = function(req, res) {
	get_list(res, req);
}