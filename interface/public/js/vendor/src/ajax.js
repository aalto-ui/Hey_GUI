(function() {

    function ajaxRequest(url, options, callbacks) {
        options = options || {};

        var xhr = new XMLHttpRequest();
        xhr.open(options.method || 'GET', url, true);

        if (typeof options.headers === 'object') {
            for (var name in options.headers) {
                var value = options.headers[name];
                xhr.setRequestHeader(name, value);
            }
        }

        if (options.type) {
            xhr.overrideMimeType(options.type);
        }

        addEvents(xhr, callbacks);
        xhr.send(options.body);

        return xhr;
    }

    // Add XHR event listeners to e.g. track progress or waiting for server data.
    function addEvents(xhr, callbacks) {
        // Monkey patching allows either a single function to be called on Ajax complete,
        // or a dictionary object with the desired Ajax events to be tracked.
        if (typeof callbacks === 'function') {
            callbacks = {
              'complete': callbacks
            }
        }

        for (var event in callbacks) {
            var cb = callbacks[event];
            if (typeof cb !== 'function') continue;

            var fn;
            switch (event) {
                case 'open':
                    fn = ajaxOpen;
                    break;
                case 'start':
                case 'loadstart':
                    fn = ajaxStart;
                    break;
                case 'progress':
                    fn = ajaxProgress;
                    break;
                case 'success':
                case 'load':
                    fn = ajaxSuccess;
                    break;
                case 'error':
                case 'abort':
                case 'timeout':
                    fn = ajaxError;
                    break;
                case 'complete':
                case 'loadend':
                case 'done':
                default:
                    fn = ajaxComplete;
                    break;
            }
            var method = fn.bind(this, xhr, cb);
            xhr.addEventListener('readystatechange', method, false);
        }
    }

    // The XHR connection has been created.
    function ajaxOpen(req, callback) {
        if (req.readyState === 1) {
            callback(req);
        }
    }

    // The XHR response headers have been received.
    function ajaxStart(req, callback) {
        if (req.readyState === 2) {
            callback(req);
        }
    }

    // The XHR response body is being received.
    function ajaxProgress(req, callback) {
        if (req.readyState === 3) {
            callback(req);
        }
    }

    // The XHR connection is successful.
    function ajaxSuccess(req, callback) {
        if (req.readyState === 4 && req.status === 200) {
            var data = response(req);
            callback(data);
        }
    }

    // The XHR connection failed.
    function ajaxError(req, callback) {
        if (req.readyState === 4 && req.status !== 200) {
            callback(req);
        }
    }

    // The XHR connection is complete, whether successfully or unsuccessfully.
    function ajaxComplete(req, callback) {
        if (req.readyState === 4) {
            if (req.status !== 200) {
                // Error happended, so set the first argument.
                callback(req);
            } else {
                // Data received successfully.
                var data = response(req);
                callback(null, data);
            }
        }
    }

    function response(req) {
        var data = req.responseText;
        // Is the response a JSON object?
        try {
            data = JSON.parse(data);
        } catch(err) {
            // Response was not a stringified object,
            // so do nothing.
        }
        return data;
    }

    // Expose library.
    window.ajax = {
        // Generic method.
        request: ajaxRequest,
        // Shorthand for retrieving arbitrary data.
        get: function(url, callbacks) {
            ajaxRequest(url, null, callbacks);
        },
        // Shorthand for submitting arbitrary data.
        post: function(url, data, callbacks) {
            ajaxRequest(url, {
                method: 'POST',
                body: data,
            }, callbacks);
        },
        // Shorthand for retrieving JSON data.
        loadJSON: function(url, callbacks) {
            ajaxRequest(url, {
                method: 'GET',
                type: 'application/json',
            }, callbacks);
        },
        // Shorthand for submitting JSON data.
        sendJSON: function(url, data, callbacks) {
            ajaxRequest(url, {
                method: 'POST',
                headers: { 'Content-type': 'application/json' },
                body: JSON.stringify(data)
            }, callbacks);
        },
    };

})();
