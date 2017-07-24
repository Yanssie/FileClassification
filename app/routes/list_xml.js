const pool = require('../models/db');

//to run a query we just pass it to the pool
//after we're done nothing has to be taken care of
//we don't have to return any client to the pool or close a connection

function get_list(res, req) {
	pool.query('SELECT * from xmlStore', function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
        	output_list(res, req, result.rows);
        }

    });

}

function output_list(res, req, rows) {
    var names = [];
    for(i = 0; i < rows.length; i++) {
      names.push(rows[i].name);
    }
    res.render('list_xml.jade', {
        		title:"List all the xml files",
        		rows: rows,
                names: names
    });
}

exports.do_work = function(req, res) {
	get_list(res, req);
}