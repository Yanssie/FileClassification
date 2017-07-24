





const pool = require('../models/db');
formidable = require('formidable');

function store_xml(res, req) {

  res.render('upload.jade', {title: "File Upload"});
}


exports.do_work = function(req, res) {
	store_xml(res, req);
}