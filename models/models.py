# -*- coding: utf-8 -*-
from odoo import models, _, api, fields
import requests
import random
import string
import logging
import json
from markupsafe import Markup

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class DiscussChannel(models.Model):
    _inherit = 'discuss.channel'

    def execute_command_ask_ai(self, **kwargs):
        key = kwargs.get('body', '').strip()
        ai_command = "/ask_ai"
        

        if key.startswith(ai_command):
            user = self.env.user
            channel = self  
            session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
            query = key[len(ai_command):].strip()  
            self.message_post(body=query, message_type='comment', subtype_xmlid='mail.mt_comment')

            if not query:
                msg = _("Please provide a query after /ask_ai.")
                channel.message_post(body=msg, message_type='comment', subtype_xmlid='mail.mt_comment', author_id=user.id)
                return

            else:
                config_rec = self.env['odoobotai.config'].search([('in_used', '=', True)], limit=1).sudo()
                if config_rec:
                    base_url = config_rec.api_url
                else:
                    base_url = 'http://host.docker.internal:8000'
                api_url = base_url.rstrip('/') + '/query/'

                payload = {
                    "model": "qwen2.5:3b",
                    "query": query,
                    "top_k": 3,
                    "user_id": user.email,
                    "session_id": session_id
                }
                try:
                    response = requests.post(api_url, data=payload, timeout=300)
                    response.raise_for_status()
                    data = response.json()
                    _logger.info(data)
                    answer = data.get("answer", "Sorry, I couldn't fetch an answer at the moment.")
                except requests.exceptions.RequestException as e:
                    _logger.error("Error fetching AI response: %s", e)
                    answer = _("Error fetching AI response: %s", str(e))
                except json.JSONDecodeError:
                    _logger.error("Error decoding JSON response")
                    answer = _("Error decoding the response from the AI service.")
                except Exception as e:
                    _logger.error("An unexpected error occurred: %s", e)
                    answer = _("An unexpected error occurred: %s", str(e))

                # Post the user's query
                # channel.message_post(body=query, message_type='comment', subtype_xmlid='mail.mt_comment', author_id=user.id)
                # Post the AI's response
                formatted_answer = "<pre>%s</pre>" % answer

                channel.message_post(
                    body=Markup("AI Response: <pre>%s</pre>") % answer,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                    author_id = 2
                )

                return


class ChatbotScriptStep(models.Model):
    _inherit = "chatbot.script.step"

    ai_response_text = fields.Text("AI Response")

    @api.model
    def execute_step(self, step_id):
        """Modify message logic to return AI response if step type is 'ai_response'."""
        step = self.browse(step_id)
        if step.step_type == "ai_response" and step.ai_response_text:
            return {
                "type": "bot_message",
                "message": step.ai_response_text,
            }
        return super(ChatbotScriptStep, self).execute_step(step_id)

    def get_next_step(self, user_input):
        """Find the next step based on user input."""
        step = self.env["chatbot.script.step"].search([("step_type", "=", "ai_response")], limit=1)

        if step:
            return step 

        return None
