"""
Email REST API views.
"""

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Email, EmailAccount
from .serializers import EmailSerializer, EmailAccountSerializer


class EmailViewSet(viewsets.ModelViewSet):
    """ViewSet for email management."""
    serializer_class = EmailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['subject', 'body_text', 'sender_email', 'sender_name']
    ordering_fields = ['received_at', 'is_read', 'category']

    def get_queryset(self):
        return Email.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark email as read."""
        email = self.get_object()
        email.is_read = True
        email.save()
        return Response({'status': 'read'})

    @action(detail=True, methods=['post'])
    def mark_unread(self, request, pk=None):
        """Mark email as unread."""
        email = self.get_object()
        email.is_read = False
        email.save()
        return Response({'status': 'unread'})

    @action(detail=True, methods=['post'])
    def summarize(self, request, pk=None):
        """AI-summarize email."""
        email = self.get_object()
        # In Phase 3, we'll actually call the AI service.
        # For now, return a placeholder.
        email.ai_summary = f"Summary: {email.snippet[:100]}..."
        email.save()
        return Response({'summary': email.ai_summary})

    @action(detail=True, methods=['post'])
    def suggest_reply(self, request, pk=None):
        """AI-suggest a reply."""
        email = self.get_object()
        # In Phase 3, we'll actually call the AI service.
        email.ai_suggested_reply = "Thank you for your email. I'll get back to you soon."
        email.save()
        return Response({'reply': email.ai_suggested_reply})

    @action(detail=False, methods=['get'])
    def folders(self, request):
        """Get summary counts for all folders."""
        queryset = self.get_queryset()
        return Response({
            'inbox': queryset.filter(folder='inbox').count(),
            'unread_inbox': queryset.filter(folder='inbox', is_read=False).count(),
            'sent': queryset.filter(folder='sent').count(),
            'draft': queryset.filter(folder='draft').count(),
            'trash': queryset.filter(folder='trash').count(),
            'important': queryset.filter(category='important').count(),
        })

class EmailAccountViewSet(viewsets.ModelViewSet):
    """ViewSet for email account configuration."""
    serializer_class = EmailAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmailAccount.objects.filter(user=self.request.user)
