var express = require("express");
var app = express();
var bodyParser = require('body-parser');
var errorHandler = require('errorhandler');
var methodOverride = require('method-override');
var fs = require('fs');
var path = require('path');

var hostname = process.env.HOSTNAME || 'localhost';
var port = 8080;

// Read data from random_payloads.json
var data = JSON.parse(fs.readFileSync(path.join(__dirname, 'random_payloads.json')));

app.get("/", function (req, res) {
    res.redirect("/plantIndex.html");
});

app.get("/getAverage", function (req, res) {
    // Modify this function if necessary
    res.send("Not implemented for file-based data");
});

app.get("/getLatest", function (req, res) {
    // Modify this function if necessary
    res.send("Not implemented for file-based data");
});

app.get("/getData", function (req, res) {
    // Modify this function if necessary
    res.send(JSON.stringify(data));
});

app.get("/getValue", function (req, res) {
    // Send the entire array of payloads
    res.send(JSON.stringify(data));
});

app.use(methodOverride());
app.use(bodyParser());
app.use(express.static(__dirname + '/public'));
app.use(errorHandler());

console.log("Simple static server listening at http://" + hostname + ":" + port);
app.listen(port);
