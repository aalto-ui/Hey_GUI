const express = require('express')
    , router  = express.Router()
    , needle  = require('needle')
    , util    = require('util')
    , fs      = require('fs')
    ;

// Work with Promises all the time.
const appendFile = util.promisify(fs.appendFile);


router.get('/', (req, res) => {
    res.render('home');
});

router.post('/intent', (req, res) => {
    let userContent = req.body;
    console.log('Intent request from editor:', JSON.stringify(userContent));

    // TODO: Edit this URL accordingly.
    let backendServer = 'http://localhost:5006/webhooks/myio/webhook';

    return needle('post', backendServer, userContent, { json: true })
    .then(response => res.json({ action: response.body }))
    .catch(err => res.status(500).send(err));
});

router.post('/notify', (req, res) => {
    // Don't log events if not running in production mode.
    if (process.env.NODE_ENV != 'production') return res.sendStatus(418);

    let userContent = req.body;
    // Add timestamp, to ease back-tracing logs.
    userContent.time = (new Date).getTime();
    // We'll use NDJSON format to store the data, so add newline.
    let line = JSON.stringify(userContent) + '\n';

    return appendFile('events.ndjson', line)
    .then(result => res.send(result))
    .catch(err => res.status(500).send(err));
});

module.exports = router;
