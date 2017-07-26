const pool = require('../models/db');
var fs = require('fs');

function get_json(res, NAME) {

    var get_query = "select * from jsonStore where name='" + NAME + "'";
	pool.query(get_query, function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
            res.render('show_json.jade', {
                NAME: NAME,
                data: result.rows[0].data
            });

        }

    });

}


exports.do_work = function(req, res){
	get_json(res,req.params.name);
};