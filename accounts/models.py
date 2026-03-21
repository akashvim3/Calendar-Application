"""
Custom User model with extended profile fields.
Supports role-based access and user preferences.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Extended user model with profile and preference fields."""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('premium', 'Premium User'),
    ]
    
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System'),
    ]
    
    # Profile fields
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    preferred_timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    
    # Preferences
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='dark')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    daily_briefing = models.BooleanField(default=True)
    
    # Google integration
    google_access_token = models.TextField(blank=True, null=True)
    google_refresh_token = models.TextField(blank=True, null=True)
    google_calendar_sync = models.BooleanField(default=False)
    gmail_sync = models.BooleanField(default=False)
    
    # AI preferences
    ai_suggestions_enabled = models.BooleanField(default=True)
    voice_assistant_enabled = models.BooleanField(default=False)
    
    # Tracking
    last_active = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    @property
    def display_name(self):
        return self.get_full_name() or self.username
    
    @property
    def initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        return self.username[0:2].upper()
