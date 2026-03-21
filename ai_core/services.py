"""
AI Core Service for Gemini Integration.
Responsible for NLP parsing, intent detection, and generating smart suggestions.
"""

import os
import google.generativeai as genai
from django.conf import settings


class GeminiService:
    """Service class for Google Gemini AI integration."""
    
    def __init__(self):
        # API Key is set in settings.py from .env
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None

    def _is_active(self):
        return self.model is not None

    def get_response(self, prompt, history=None):
        """Get standard conversational response."""
        if not self._is_active():
            return "AI service is currently unavailable. Please configure API key."
        
        try:
            if history:
                # history format: [{'role': 'user', 'parts': [content]}, ...]
                chat = self.model.start_chat(history=history)
                response = chat.send_message(prompt)
            else:
                response = self.model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            return f"Error connecting to AI: {str(e)}"

    def detect_intent(self, text):
        """
        Detect user intent from natural language.
        Returns JSON-like structure with action, parameters.
        """
        if not self._is_active():
            return {'action': 'none', 'msg': 'API not configured'}

        prompt = f"""
        Analyze the following user input and detect the intent. 
        Possible intents are: 'create_event', 'create_task', 'send_email', 'search_email', 'summarize', 'query'.
        Return the response in JSON format.
        
        Text: '{text}'
        
        Example JSON response:
        {{
            "intent": "create_event",
            "confidence": 0.95,
            "parameters": {{
                "title": "Project Meeting",
                "start_time": "2026-03-20 10:00:00",
                "end_time": "2026-03-20 11:00:00"
            }}
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Simple fallback (Phase 3 would have robust JSON parsing)
            return response.text
        except Exception:
            return None

    def get_smart_suggestions(self, context=None):
        """Generate smart suggestions based on user context."""
        # This will be refined as the user interacts.
        pass
