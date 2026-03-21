"""
Email models for inbox management and AI integration.
Supports Gmail synchronization, AI replies, and smart categorization.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class EmailAccount(models.Model):
    """Google/Gmail account connection status."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_account')
    email_address = models.EmailField()
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expiry = models.DateTimeField()
    last_sync = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email_address} ({self.user.username})"


class Email(models.Model):
    """Local representation of a Gmail message."""
    
    FOLDER_CHOICES = [
        ('inbox', 'Inbox'),
        ('sent', 'Sent'),
        ('draft', 'Draft'),
        ('trash', 'Trash'),
        ('spam', 'Spam'),
    ]
    
    CATEGORY_CHOICES = [
        ('important', 'Important'),
        ('personal', 'Personal'),
        ('promotions', 'Promotions'),
        ('social', 'Social'),
        ('updates', 'Updates'),
        ('forums', 'Forums'),
    ]
    
    # Message ID from Gmail
    gmail_message_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    thread_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Basic Info
    sender_email = models.EmailField()
    sender_name = models.CharField(max_length=255, blank=True)
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body_text = models.TextField(blank=True)
    body_html = models.TextField(blank=True)
    snippet = models.TextField(max_length=500, blank=True)
    
    # Metadata
    received_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    folder = models.CharField(max_length=20, choices=FOLDER_CHOICES, default='inbox')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')
    
    # AI Support
    ai_summary = models.TextField(blank=True)
    ai_suggested_reply = models.TextField(blank=True)
    ai_intent_detected = models.CharField(max_length=50, blank=True)
    
    # Meta
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emails')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'emails'
        ordering = ['-received_at']
        indexes = [
            models.Index(fields=['user', 'received_at']),
            models.Index(fields=['gmail_message_id']),
            models.Index(fields=['thread_id']),
        ]

    def __str__(self):
        return f"{self.subject[:50]} from {self.sender_email}"
