"""Account admin configuration."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin for the User model."""
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'is_active']
    list_filter = ['role', 'is_verified', 'is_active', 'theme']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {
            'fields': ('avatar', 'bio', 'phone', 'role', 'preferred_timezone')
        }),
        ('Preferences', {
            'fields': ('theme', 'email_notifications', 'push_notifications', 
                       'daily_briefing', 'ai_suggestions_enabled', 'voice_assistant_enabled')
        }),
        ('Google Integration', {
            'fields': ('google_calendar_sync', 'gmail_sync'),
            'classes': ('collapse',),
        }),
    )
