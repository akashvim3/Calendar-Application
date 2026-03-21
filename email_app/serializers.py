"""Email app serializers."""

from rest_framework import serializers
from .models import Email, EmailAccount


class EmailAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAccount
        fields = ['id', 'email_address', 'last_sync', 'is_active']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = [
            'id', 'gmail_message_id', 'thread_id', 'sender_email', 'sender_name',
            'recipient_email', 'subject', 'body_text', 'body_html', 'snippet',
            'received_at', 'is_read', 'folder', 'category', 'ai_summary',
            'ai_suggested_reply', 'ai_intent_detected',
        ]
        read_only_fields = ['received_at', 'ai_summary', 'ai_suggested_reply', 'ai_intent_detected']
