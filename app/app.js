var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var multer = require('multer');
var upload_multer = multer({dest:'./uploads/'});
var fs = require('fs');
var PythonShell = require('python-shell');

var index = require('./routes/index');
var users = require('./routes/users');
var upload = require('./routes/upload');
var list = require('./routes/list');
var list_xml = require('./routes/list_xml');
var list_json = require('./routes/list_json');
var show_json = require('./routes/show_json');
var show_xml = require('./routes/show_xml');
var upload_json = require('./routes/upload_json');
var cluster = require('./routes/cluster');

var app = express();


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// app.use(multer);

app.use('/', index);
app.use('/users', users);

app.get('/upload', upload.do_work);
app.get('/list', list.do_work);
app.get('/list_xml', list_xml.do_work);
app.get('/list_json', list_json.do_work);
app.get('/show_json/:name', show_json.do_work);
app.get('/show_xml/:name', show_xml.do_work);
app.get('/upload_json', upload_json.do_work);
app.get('/cluster', cluster.do_work);
app.get('/ajax_get_json', cluster.ajax_work);


app.post('/list', list.do_work_post);

const pool = require('./models/db');
// handle the post request from /upload
app.post('/upload', upload_multer.any(), function (request, res, next) {
  //req.files have multiple files
  console.log(request.files);
  var title_all = [];
  var title_all_dup = [];
  var size_all = [];
  for(i=0; i<request.files.length; i++) {
      var title = request.files[i].originalname; 
      title_all.push(title);
      title_all_dup.push(title);
      var size = request.files[i].size;
      size_all.push(size);
  }
  var data_all = [];
  for (j = request.files.length - 1; j >= 0; j--) {
    // upload datas into database
      var fs_path = request.files[j].path;
      fs.readFile(fs_path, 'utf8', function (err, data) {
          if (err) throw err;
          // console.log(title_all.pop());
          data_all.push(data);
          var title = title_all.pop();
          // data will contain your file contents
          // store data into database
          // console.log("[DATA] " + data);
          queryString = "insert into xmlstore values ('" + title.substring(0, title.length-4) + "','" + data + "');"
          // console.log(queryString)
          pool.query(queryString, function(err, result) {
            if(err) {
              if(err.code==23505) {
                console.log('duplicate file name ' + title);
              }
              if(err.code=='2200N') {
                console.log('Invalid XML Content');
              }
              return console.error('error running query', title, err);
            }else {
              console.log('successfully uploaded ' + title);
              /** extract activities to json files **/
              // extract each xml from database and convert to json
              extract_json(title);
              // delete origin file
              if (fs.existsSync(fs_path)) {
                fs.unlink(fs_path, function (err) {
                  if (err) throw err;
                  console.log('successfully deleted fs file! ' + fs_path);
                }); 
              }
              
            }

          });


        });

  }
  // res.send({redirect: '/list'});
  // res.render('upload');        
  // res.render('upload_file.jade', {
  //               success: "Upload successfully!",
  //               title: title_all,
  //               size: size_all
  //             });
  
  
})
function extract_json(title) {
  console.log('[EXTRACT]')
  var name = title.substring(0, title.length-4);
  var get_xml_query = "select * from xmlStore where name='" + name + "';"
  pool.query(get_xml_query, function(err, result) {
        if(err) {
          return console.error('error running query', err);
        } else {
          // console.log("[RESULT] " + result.rows[0].data);
          // write xml files to uploads folder
          fs.writeFile(__dirname + "/uploads/" + name + ".xml", result.rows[0].data, function(err) {
                  if(err) {
                   return console.log(err);
                  }
                  console.log("The xml file was downloaded!");
                  // run python script
                var options = {
                  mode: 'text',
                  scriptPath: __dirname + '/script/',
                  args: [__dirname+'/library', __dirname+'/uploads', name]
                };

                PythonShell.run('newParser.py', options, function (err, results) {
                    if (err) throw err;
                    // results is an array consisting of messages collected during execution
                    console.log('results: %j', results);
                    console.log("finished writing json file!");
                    /** upload json file **/
                    upload_json_file(name);
                });
              
              }); 

        }
      });
}
function upload_json_file(name) {
  var json_path = __dirname + "/uploads/" + name + ".xml.json";
    // console.log(json_path)
    fs.readFile(json_path, 'utf8', function (err, data) {
        console.log(json_path)
        if (err) throw err;
        var query = "insert into jsonStore values('" + name + "','" + data + "');"
        pool.query(query, function(err, result) {
            if(err) {
                if(err.code==23505) {
                    console.log("duplicate json file!");
                }
                return console.error('error running query', err);
            } else {
                console.log("successfully uploaded json!")
                // delete_file(name);
            }

        });

    });
}
// delete xml and json files located in local uploads files
function delete_file(NAME) {

    // delete file
    var xml_path = __dirname + "/uploads/" + NAME + ".xml";
    fs.unlink(xml_path, function (err) {
      if (err) throw err;
      console.log('successfully deleted ' + xml_path);
    });   

    var json_path = __dirname + "/uploads/" + NAME + ".xml.json";
    fs.unlink(json_path, function (err) {
      if (err) throw err;
      console.log('successfully deleted ' + json_path);
    }); 
}


// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
