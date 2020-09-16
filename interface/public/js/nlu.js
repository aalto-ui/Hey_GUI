window.NLU = {

    intent: function(obj) {
        // We can receive multiple responses from the NLU server in the same request.
        for (var i = 0; i < obj.action.length; i++) {
            var action = obj.action[i];
            console.log('Command:', action);

            if (action.custom) {
                var command = JSON.parse(action.custom);

                if (command.intent == 'object') {
                    // Not implemented.
                } else if (command.intent == 'suggest') {
                    // Here, the user should have been provided with several design suggestions before,
                    // and one of these suggestions has been selected.
                    if (command.result) {
                        // TODO
                    }
                } else if (command.intent == 'recommend_topic' || command.intent == 'recommend_category') {
                    // Ensure that we get some data, otherwise the bot will forward the error from the NLU server.
                    if (command.result) {
                        // TODO
                    }
                } else {
                    console.warn('Unknown intent: %s', command.intent);
                }
            }

            if (action.text) {
                Chatbot.response(action.text);
            }
        }
    },

};
