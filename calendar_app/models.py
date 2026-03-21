"""
Calendar models for event management.
Supports recurring events, categories, and timezone-aware scheduling.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class EventCategory(models.Model):
    """Categories for calendar events."""
    
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#6366f1')  # Hex color
    icon = models.CharField(max_length=50, default='calendar')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_categories')
    
    class Meta:
        db_table = 'event_categories'
        verbose_name_plural = 'Event Categories'
        unique_together = ['name', 'user']
    
    def __str__(self):
        return self.name


class Event(models.Model):
    """Calendar event model with full scheduling support."""
    
    RECURRENCE_CHOICES = [
        ('none', 'No Recurrence'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic fields
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=300, blank=True)
    
    # Timing
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    all_day = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    
    # Categorization
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    color = models.CharField(max_length=7, default='#6366f1')
    
    # Recurrence
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default='none')
    recurrence_end = models.DateField(null=True, blank=True)
    
    # Attendees & Reminders
    reminder_minutes = models.IntegerField(default=30)
    
    # Meeting link
    meeting_link = models.URLField(blank=True)
    meeting_notes = models.TextField(blank=True)
    
    # Google Calendar sync
    google_event_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Meta
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'events'
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['user', 'start_time']),
            models.Index(fields=['start_time', 'end_time']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
    
    @property
    def duration_minutes(self):
        """Get event duration in minutes."""
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)
    
    @property
    def is_past(self):
        return self.end_time < timezone.now()
    
    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time
