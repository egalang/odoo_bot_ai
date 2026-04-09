// odoo.define('custom_chatbot_api.chat_extension', function (require) {
//     "use strict";
    
//     var ajax = require('web.ajax');
//     // Attempt to get the Live Chat widget. Depending on your Odoo version,
//     // the module name may vary. Here we assume it is defined in 'website_livechat.livechat'.
//     var LiveChat = require('website_livechat.livechat');

//     if (LiveChat) {
//         // Extend the widget by overriding the message send handler.
//         LiveChat.include({
//             /**
//              * Override the sendMessage function (or the equivalent event handler)
//              * so that instead of calling the default /mail/message/post endpoint,
//              * it calls our custom endpoint.
//              */
//             sendMessage: function () {
//                 var self = this;
//                 // Get the user's message from the input.
//                 var $input = this.$el.find('.o_livechat_input');
//                 var message = $input.val().trim();
//                 if (!message) {
//                     return;
//                 }
//                 // Clear the input field.
//                 $input.val('');
//                 // Log for debugging.
//                 console.log("Custom sendMessage triggered with message:", message);
//                 // Instead of posting directly to /mail/message/post,
//                 // call our custom endpoint via ajax.jsonRpc.
//                 ajax.jsonRpc('/custom_chatbot/respond', 'call', { query: message })
//                     .then(function (result) {
//                         // Append the user's message and then the bot's reply.
//                         self._appendMessage('user', message);
//                         self._appendMessage('bot', result.answer);
//                     })
//                     .fail(function (err) {
//                         self._appendMessage('bot', "Error: Unable to get response from API.");
//                     });
//             },

//             /**
//              * Helper function to append a message to the chat history.
//              * Adjust the HTML structure and classes as needed.
//              *
//              * @param {string} sender - 'user' or 'bot'
//              * @param {string} text - The message text
//              */
//             _appendMessage: function (sender, text) {
//                 var messageHtml = '<div class="o_livechat_message ' + sender + '">' + text + '</div>';
//                 var $history = this.$el.find('.o_livechat_history');
//                 $history.append(messageHtml);
//                 // Optionally scroll to the bottom.
//                 $history.scrollTop($history[0].scrollHeight);
//             }
//         });
//         console.log("Custom chat_extension module loaded and widget overridden.");
//     } else {
//         console.error("LiveChat widget not found. Check module dependencies and names.");
//     }
// });
