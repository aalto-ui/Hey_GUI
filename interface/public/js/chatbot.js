if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    console.warn('This browser does not accept speech input.');
}

var sessionId = (Math.random().toString(36) + Date.now()).substr(2);

navigator.mediaDevices.getUserMedia({audio: true})
    .then(function(instance) {
        var chatInputEl = document.querySelector('input.speech-input');
        // If the data-instant-submit attribute is not set,
        // we can still get notified via callbacks.
        chatInputEl.onvoiceend = function() {
            submit(this.value, NLU.intent);
        };
    })
    .catch(function(err) {
        botResponse('Please ensure your microphone is working.');
        console.warn(err);
    });

/**
 * Allow to navigate back and forth the issued commands or utterances.
 * @class
 * @param {string} inputEl - Text input field.
 */
function Commander(inputEl) {
    let history = [];
    let index = 0;
    // Store a new utterance in the stack.
    this.save = function() {
        if (inputEl.value) {
            history.push(inputEl.value);
            index = history.length;
        }
    };
    /* @private */
    function restore(index) {
        if (history[index]) {
            inputEl.value = history[index];
        }
    };
    // Go back to the previously entered sentence, if any.
    this.up = function() {
        if (index > 0) {
            index--;
            restore(index);
        }
    };
    // Go forward to the next-entered sentence, if any.
    this.down = function() {
        if (index < history.length - 1) {
            index++;
            restore(index);
        }
    };
}

const msgerForm = document.querySelector('.msger-inputarea');
const msgerInput = document.querySelector('.msger-input');
const msgerChat = document.querySelector('.msger-chat');

// Bind command history manager to the input text field.
const cmdHistory = new Commander(msgerInput);

// Don't call the default SUBMIT action to prevent a page refresh.
msgerForm.addEventListener('submit', function(event) {
    event.preventDefault();
    submitForm();
});

// But simulate the expected behavior when hitting the ENTER key.
msgerInput.addEventListener('keypress', function(event) {
    if (event.keyCode == 13) {
        cmdHistory.save();

        event.preventDefault();
        submitForm();
    }
});

// Arrow commands are non-printable, so we must listen to keyup/down events.
msgerInput.addEventListener('keyup', function(event) {
    if (event.keyCode == 38) {
        event.preventDefault();
        cmdHistory.up();
    } else if (event.keyCode == 40) {
        event.preventDefault();
        cmdHistory.down();
    }
});

function submitForm() {
    const msgText = msgerInput.value;
    if (!msgText) return;

    userQuery(msgText);

    submit(msgText, function(res) {
        msgerInput.value = '';
        NLU.intent(res);
    });
}

// Greeting.
botResponse('Hi! Say "Help" or write some message.');

function appendMessage(name, img, side, text) {
    // NB: Ensure that the NLU server always return HTML.
    const msgHTML = `
      <div class="msg ${side}-msg">
        <div class="msg-img" style="background-image: url(${img})"></div>

        <div class="msg-bubble">
          <div class="msg-info">
            <div class="msg-info-name">${name}</div>
            <div class="msg-info-time">${formatDate(new Date())}</div>
          </div>

          <div class="msg-text">${text}</div>
        </div>
      </div>
    `;

    msgerChat.insertAdjacentHTML('beforeend', msgHTML);
    msgerChat.scrollTop += 500;
}

function formatDate(date) {
    const h = '0' + date.getHours();
    const m = '0' + date.getMinutes();

    return `${h.slice(-2)}:${m.slice(-2)}`;
}

function userQuery(msgText) {
    appendMessage('You', 'user.svg', 'right', msgText);
}

function botResponse(msgText) {
    appendMessage('Bot', 'bot.svg', 'left', msgText);
}

function submit(sentence, callback) {
    const payload = {sender: sessionId, message: sentence};
    logInteraction('submit', payload);

    ajax.request('/intent', {
        method: 'POST',
        headers: {'Content-type': 'application/json'},
        body: JSON.stringify(payload),
    }, {
        // Request has started.
        open: function() {
            msgerInput.readOnly = true;
        },
        // Request has failed.
        error: function(err) {
            // XHR events are not serializable, so pick the relevant parts.
            logInteraction('error', {
                responseText: err.responseText,
                status: err.status,
                statusText: err.statusText,
            });
            // var msg = `Sorry, got ${err.status} error: ${err.responseText}`;
            var msg = `Sorry, I cannot handle your request (${err.status} error). Please try again later.`;
            return botResponse(msg);
        },
        // Request has succeeded.
        success: function(data) {
            logInteraction('success', data);
            callback(data);
        },
        // Request has finished, whether successfully or unsuccessfully.
        done: function() {
            msgerInput.readOnly = false;
        },
    });
}

function logInteraction(type, data) {
    // We don't care if this request doesn't reach the server.
    // We just send the data for later evaluation.
    ajax.request('/notify', {
        method: 'POST',
        headers: {'Content-type': 'application/json'},
        body: JSON.stringify({type: type, data: data}),
    });
}

// Expose main methods so that other modules can use them.
window.Chatbot = {

    response: botResponse,
    submit: submit,

};
