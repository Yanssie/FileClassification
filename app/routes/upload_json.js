const pool = require('../models/db');
var fs = require('fs');

function upload_json(res, NAME) {
    var json_path = __dirname + "/../uploads/" + NAME + ".xml.json";
    fs.readFile(json_path, 'utf8', function (err, data) {
        if (err) throw err;
        var query = "insert into jsonStore values('" + NAME + "','" + data + "');";
        pool.query(query, function(err, result) {
            if(err) {
                if(err.code==23505) {
                    res.render('show_json.jade', {
                        title:"Splitted graph of " + NAME,
                        NAME: NAME,
                        data: data,
                        success: "Duplicate File"
                    });
                    delete_file(NAME);
                }
                return console.error('error running query', err);
            } else {
                console.log("successfully uploaded json!")
                res.render('show_json.jade', {
                    title:"Splitted graph of " + NAME,
                    NAME: NAME,
                    data: data,
                    success: "Upload successfully"
                });

                delete_file(NAME);
            }

        });

    });

}

function delete_file(NAME) {
    // delete file
    console.log("file name" + NAME);
    var xml_path = __dirname + "/../uploads/" + NAME + ".xml";
    fs.unlink(xml_path, function (err) {
      if (err) throw err;
      console.log('successfully deleted ' + xml_path);
    });   

    var json_path = __dirname + "/../uploads/" + NAME + ".xml.json";
    fs.unlink(json_path, function (err) {
      if (err) throw err;
      console.log('successfully deleted ' + json_path);
    }); 
}



exports.do_work = function(req, res){
	upload_json(res,req.query.NAME);
};