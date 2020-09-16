/*global webkitSpeechRecognition */
(function() {
  'use strict';

  // Check for ASR support (currently webkit only).
  if (!('webkitSpeechRecognition' in window)) return;

  document.addEventListener('DOMContentLoaded', function(ev) {

      // ASR ready text placeholder.
      var defaultReadyText = 'Speak now';
      // Seconds to wait for more user utterance.
      var defaultPatience = 6;

      var inputEls = document.getElementsByClassName('speech-input');
      [].forEach.call(inputEls, function(inputEl) {

          var parent = inputEl.parentNode;
          var micBtn = parent.querySelector('.speech-input-btn');

          if (!micBtn) {
              var icon = inputEl.dataset.icon || 'mic.svg';
              var size = inputEl.dataset.iconSize || inputEl.offsetHeight;

              micBtn = document.createElement('input');
              micBtn.classList.add('speech-input-btn');
              micBtn.type = 'image';
              micBtn.src = icon;
              micBtn.style = 'width:' + size + 'px; height:' + size + 'px';
              micBtn.alt = 'mic';

    		      parent.insertBefore(micBtn, inputEl.nextSibling);
          }

          // Setup recognition.
          var recognizing = false;
          var timeout, inputPlaceholder;

          var recognition = new webkitSpeechRecognition();
          recognition.continuous = true;
          recognition.interimResults = true;

          if (inputEl.lang) recognition.lang = inputEl.lang;

          var patience = parseInt(inputEl.dataset.patience, 10) || defaultPatience;

          function restartTimer() {
              timeout = setTimeout(function() {
                  recognition.stop();
              }, patience * 1000);
          }

          recognition.onstart = function() {
              // Inform that ASR is ready.
              inputPlaceholder = inputEl.placeholder;
              inputEl.placeholder = inputEl.dataset.readyText || defaultReadyText;

              recognizing = true;
              inputEl.classList.add('listening');

              // Callback.
              if (typeof inputEl.onvoicestart == 'function') inputEl.onvoicestart();

              restartTimer();
          };

          recognition.onend = function() {
              clearTimeout(timeout);

              recognizing = false;
              inputEl.classList.remove('listening');

              if (inputPlaceholder !== null) inputEl.placeholder = inputPlaceholder;

              // Callback.
              if (typeof inputEl.onvoiceend == 'function') inputEl.onvoiceend();

              // Auto-submit form if set.
              if (inputEl.dataset.instantSubmit && inputEl.value && inputEl.form) {
                  inputEl.form.submit();
              }
          };

          recognition.onresult = function(event) {
              clearTimeout(timeout);

              var resultList = event.results;

              // Go through each SpeechRecognitionResult object in the list.
              var finalTranscript = '';
              var interimTranscript = '';
              for (var i = event.resultIndex; i < resultList.length; ++i) {
                  var result = resultList[i];

                  // Get this result's first SpeechRecognitionAlternative object.
                  var firstAlternative = result[0];

                  if (result.isFinal) {
                      finalTranscript = firstAlternative.transcript;
                  } else {
                      interimTranscript += firstAlternative.transcript;
                  }
              }

              var transcript = finalTranscript || interimTranscript;

              // Modify the query to the new transcript.
              inputEl.value = transcript;
              inputEl.focus();

              if (inputEl.tagName === 'INPUT') {
                  inputEl.scrollLeft = inputEl.scrollWidth;
              } else {
                  inputEl.scrollTop = inputEl.scrollHeight;
              }

              // Callback.
              if (typeof inputEl.onvoiceinput == 'function') inputEl.onvoiceinput();

              restartTimer();
          };

          micBtn.addEventListener('click', function(event) {
              event.preventDefault();

              // Prevent recording on implicit form submission;
              // e.g. when the user hits the Enter key on a text field.
              if (!event.clientX && !event.clientY) return;

              if (recognizing) {
                  recognition.stop();
                  return;
              }

              recognition.start();
          });

      }); // end forEach

  });
})();
