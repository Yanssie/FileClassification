const pool = require('../models/db');
var fs = require('fs');

function get_xml(res, NAME) {

	var get_query = "select * from xmlStore where name='" + NAME + "'";
	pool.query(get_query, function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
            res.render('show_xml.jade', {
                NAME: NAME,
                data: result.rows[0].data
            });

        }

    });

}


exports.do_work = function(req, res){
	get_xml(res,req.params.name);
};