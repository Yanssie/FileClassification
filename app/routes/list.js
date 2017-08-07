const pool = require('../models/db');
var fs = require('fs');
var path = require('path');
var PythonShell = require('python-shell');

exports.do_work = function(req, res) {
    get_list(res, req);
}

exports.do_work_post = function(req, res) {
    extract_features(res, req);
}

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

function extract_features(res, req) {
    console.log("runnning post!")
    // query = "select * from jsonstore; "
    // pool.query(query, function(err, result) {
    //     if(err) {
    //       return console.error('error running query', err);
    //     } else {
    //         for (i=0; i<result.rows.length; i++) {
    //             fs.writeFile(__dirname + "/../split/" + result.rows[i].name + ".json", result.rows[i].data, function(err) {
    //               if(err) {
    //                return console.log(err);
    //               }
    //               console.log("The json file was downloaded!");
              
    //             }); 
    //         }
            
    //     }

    // });

    // run python script
                var options = {
                  mode: 'text',
                  scriptPath: __dirname + '/../script/',
                  args: [__dirname+'/../uploads']
                };
                
            try {
                PythonShell.run('LoadJson.py', options, function (err, results) {
                    if (err) throw err;
                    // results is an array consisting of messages collected during execution
                    console.log('[results:]')
                    feature_names = results[1]
                    feature_names = feature_names.replace('[','');
                    feature_names = feature_names.replace(']','');
                    feature_names = feature_names.split(',')

                    vectors = results[2]
                    vectors = vectors.replace('[[', '[')
                    vectors = vectors.replace(']]', ']')
                    vectors = vectors.replace(/],/g, ']],')
                    vectors = vectors.split('], ')

                    pred_result = results[3]
                    pred_result = pred_result.split(' ')
                    console.log("finished extracting features!")
                    upload_features(res, req, feature_names, vectors, pred_result);
                });
            } catch(ex) {

            }
}

function upload_features(res, req, feature_names, vectors, pred_result) {
    query = ""
    for (i=0; i<feature_names.length; i++) {
        query += "insert into features values(" + feature_names[i].substring(0, feature_names[i].length-10) + "','" + vectors[i] + "','" + pred_result[i] + "');"
    }
    pool.query(query, function(err, result) {
        if(err) {
            if(err.code==23505) {
                console.log('duplicate file name');
                return;
              }
            return console.error('error running query', err);
        } else {
            console.log("finished upload features!")
            // delete_files();
            // use 
            
        }

    });
}

function delete_files() {
    var dir = __dirname+'/../uploads';

    fs.readdir(dir, (err, files) => {
        if (err) throw error;
        for (const file of files) {
            fs.unlink(path.join(dir, file), err => {
                if (err) throw error;
            });
        }
        console.log('delete files in uploads!')
    });
}

