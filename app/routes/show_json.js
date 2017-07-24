const pool = require('../models/db');
var fs = require('fs');
var PythonShell = require('python-shell');

function get_xml(res, NAME) {

	var get_query = "select * from xmlStore where name='" + NAME + "'";
	pool.query(get_query, function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
        	fs.writeFile(__dirname + "/../uploads/" + NAME + ".xml", result.rows[0].data, function(err) {
                if(err) {
                return console.log(err);
                }
                console.log("The xml file was saved!");

                var options = {
                	mode: 'text',
                	scriptPath: __dirname + '/../script/',
                    args: [__dirname+'/../../library', __dirname+'/../uploads']
                };

                PythonShell.run('newParser.py', options, function (err, results) {
                    if (err) throw err;
                    // results is an array consisting of messages collected during execution
                    console.log('results: %j', results);
                    console.log("finished writing json file");
                });
              
            }); 


            get_json(res, NAME);
        }

    });

}

// read generated json file and send to show_json.jade
function get_json(res, NAME) {
	var json_path = __dirname + "/../uploads/" + NAME + ".xml.json";
	fs.readFile(json_path, 'utf8', function (err, data) {
        if (err) throw err;
        res.render('show_json.jade', {
        		title:"Splitted graph of " + NAME,
        		NAME: NAME,
                data: data
        });
    });
}


exports.do_work = function(req, res){
	get_xml(res,req.query.NAME);
};