"""
Chat app models for conversational AI.
Stores chat history, AI context, and action triggers.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class ChatSession(models.Model):
    """A single chat conversation session."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=255, default='New Chat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    """Individual message within a chat session."""
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'AI Assistant'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    
    # Audio/Voice support
    audio_file = models.FileField(upload_to='chat_audio/', null=True, blank=True)
    
    # AI Metadata
    intent = models.CharField(max_length=100, blank=True)  # email, calendar, task, query
    action_triggered = models.BooleanField(default=False)
    action_type = models.CharField(max_length=50, blank=True)
    action_data = models.JSONField(null=True, blank=True)
    
    # Timing
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'chat_messages'
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
