var $ = require('jquery');

$("#xml_table tr").click(function(){
   $(this).addClass('selected').siblings().removeClass('selected');    
   var value=$(this).find('td:first').text;
   alert(value);    
});
// var table = document.getElementById("xml_table");
// alert(table.rows.length);  
// console.log(table.rows.length);