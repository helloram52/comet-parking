var express = require('express');
var router = express.Router();
var request = require('request');
var utilities = require('../lib/utilities');
var fs = require('fs');
var outputFile = './public/data/processeddata.json';

/* GET home page. */
router.get('/', function(request, response) {
});

router.get('/detect', function(request, response) {
	response.json(JSON.parse(fs.readFileSync(outputFile)));
});

module.exports = router;