"""AI core API views."""

from rest_framework import views, permissions, response, status
from .services import GeminiService


class GeminiChatView(views.APIView):
    """API endpoint to chat with Gemini AI."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt')
        history = request.data.get('history', [])

        if not prompt:
            return response.Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = GeminiService()
        ai_response = service.get_response(prompt, history)
        
        return response.Response({'response': ai_response})


class IntentDetectionView(views.APIView):
    """API endpoint to detect intent from text."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        text = request.data.get('text')
        if not text:
            return response.Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = GeminiService()
        intent = service.detect_intent(text)
        
        return response.Response({'intent': intent})


# URL definitions removed from here, they are in api_urls.py
