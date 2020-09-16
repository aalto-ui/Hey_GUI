const express = require('express');
const bodyParser = require('body-parser');
const pkg = require('./package.json');
const app = express();

// FIXME: Make the port number configurable.
const port = 3000;

// Set up template engine.
// TODO: Maybe make the engine configurable as well.
const mustacheExpress = require('mustache-express');
app.engine('mustache', mustacheExpress());
app.set('view engine', 'mustache');
app.set('views', __dirname + '/views');

// Serve static assets.
app.use(express.static(__dirname + '/public'));

// Accept POST requests; i.e. application/x-www-form-urlencoded data.
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Set up routes.
var routes = require('./routes');
app.use('/', routes);

// Launch app.
app.listen(port, () => console.log(`App ${pkg.name} runing on port ${port}!`));
