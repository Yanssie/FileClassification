const pool = require('../models/db');


function get_list(res, req) {
    query = "select xmlstore.name, xmlstore.data as xml_data, jsonstore.data as json_data "
	query += "from xmlstore, jsonstore where xmlstore.name=jsonstore.name;"
    pool.query(query, function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
        	output_list(res, req, result.rows);
        }

    });

}

function output_list(res, req, rows) {
    res.render('list.jade', {
        		title:"List all the files",
        		rows: rows
    });
}

exports.do_work = function(req, res) {
	get_list(res, req);
}