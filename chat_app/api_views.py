"""
Chat REST API views.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer


class ChatSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for chat session management."""
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send message to AI assistant."""
        session = self.get_object()
        content = request.data.get('content')
        
        if not content:
            return Response({'error': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            role='user',
            content=content
        )
        
        # 2. Process with AI (Placeholder for now)
        # In Phase 3, we'll actually call the Gemini service.
        ai_response_content = f"I've received your message: '{content}'. How can I help you today?"
        
        # 3. Save assistant message
        ai_message = ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=ai_response_content
        )
        
        return Response({
            'user_message': ChatMessageSerializer(user_message).data,
            'assistant_message': ChatMessageSerializer(ai_message).data
        })

class ChatMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """ReadOnly viewset for messages."""
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(session__user=self.request.user)
