"""
Notifications model and management.
Supports in-app, email, and push notifications via Firebase.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Notification(models.Model):
    """Notification model for user alerts."""
    
    TYPE_CHOICES = [
        ('event_reminder', 'Event Reminder'),
        ('task_reminder', 'Task Reminder'),
        ('email_reply', 'Email Reply Received'),
        ('system_alert', 'System Alert'),
        ('ai_suggestion', 'AI Suggestion'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Status
    is_read = models.BooleanField(default=False)
    is_pushed = models.BooleanField(default=False)  # FCM push
    is_emailed = models.BooleanField(default=False) # Email sent
    
    # Data for frontend action
    action_url = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    @property
    def time_since(self):
        """Relative time since creation."""
        from django.utils.timesince import timesince
        return timesince(self.created_at)
