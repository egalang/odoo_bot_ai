# -*- coding: utf-8 -*-
import random
import string
import requests
from odoo import http
from odoo.http import request


class ChatbotController(http.Controller):

    @http.route('/chatbot/ai', type='http', auth='user', methods=['GET'], csrf=False)
    def chatbot_ai(self, query, **kwargs):
        """ Odoo bot will call this endpoint to get AI responses """

        user = request.env.user
        session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        
        api_url = "https://your-api-endpoint.com/query"
        payload = {
            "query": query,
            "top_k": 3,
            "user_id": user.email,
            "session_id": session_id
        }

        try:
            response = requests.get(api_url, params=payload, timeout=5)
            data = response.json()
            answer = data.get("answer", "No response available.")
        except Exception as e:
            answer = "Error: " + str(e)

        return answer
