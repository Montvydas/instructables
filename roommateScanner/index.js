require('dotenv').config();

const PythonShell = require('python-shell');
// const fs = require('fs');
const express = require('express');
const bodyParser= require('body-parser');
// const path = require('path')
const app = express();

const http = require('http');
const url = require('url');

let key = 'IFTTT_KEY';


function scriptString(){
    return './public/python/test.py'
}

//Server Configuration
app.use(bodyParser.urlencoded({ extended: true }))
app.use(express.static(__dirname + '/public'));

// frontend goes into the public folder as index.html
app.get('/', function(req, res){
    res.sendFile('index');
})

app.get('/api/flatmates', function(req, res){
    // res.send("went into /api/flatmates")
    if (req.query.password === process.env.PASS){
        PythonShell.run(scriptString(), function (err, pythonRes) {
            console.log(pythonRes[0])
            res.send(pythonRes[0])
            triggerIftttMakerWebhook('request-to-text', key, pythonRes[0]);
            // run the script here to perform a post request!!!
        });
    } else {
        res.send("invalid password, try again!")
    }
})

app.listen(process.env.PORT, function(){
    console.log('Listening on port ' + process.env.PORT);
})

function triggerIftttMakerWebhook(event, key, value1, value2, value3) {
    let iftttNotificationUrl = `https://maker.ifttt.com/trigger/${event}/with/key/${key}`;
    let postData = JSON.stringify({ value1, value2, value3 });

    console.log(postData)

    var parsedUrl = url.parse(iftttNotificationUrl);
    var post_options = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port,
        path: parsedUrl.path,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': postData.length
        }
    };

    // Set up the request
    var post_req = http.request(post_options, function(res) {
        res.setEncoding('utf8');
        res.on('data', function (chunk) {
            console.log('Response: ' + chunk);
        });
    });

    // Trigger a POST to the url with the body.
    post_req.write(postData);
    post_req.end();
}
