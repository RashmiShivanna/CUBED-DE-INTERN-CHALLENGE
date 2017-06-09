
var express = require("express");
var app = express();

app.get('/', function (req, res) 
{  
    var sql = require("mssql");
    // config for your database
    var config = 
	{
        user: 'sa',
		password: 'password',
        server: 'localhost\\SQLEXPRESS', 
        database: 'Amazon' 
    };

    // connect to your database
    sql.connect(config, function (err) 
	{   
        if (err) console.log(err);
        // create Request object
        var request = new sql.Request();
           
        // query to the database and get the records
        request.query('select top 10 * from ProductList', function(err,recordset)
		{			
		res.send(recordset)	
		
		});	
    });

});

var server = app.listen(5000, function () {
    console.log('Server is running..');
});