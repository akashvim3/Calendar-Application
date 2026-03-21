"""
Tasks and Reminders models.
Supports NLP parsing, priority levels, and progress tracking.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class TaskCategory(models.Model):
    """Categories for tasks."""
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#6366f1')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_categories')

    class Meta:
        db_table = 'task_categories'
        verbose_name_plural = 'Task Categories'
        unique_together = ['name', 'user']

    def __str__(self):
        return self.name


class Task(models.Model):
    """Task model with reminder support."""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    # Priority and Status
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    progress = models.IntegerField(default=0)  # 0 to 100
    
    # Categorization
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    
    # Reminders
    reminder_sent = models.BooleanField(default=False)
    reminder_at = models.DateTimeField(null=True, blank=True)
    
    # Meta
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tasks'
        ordering = ['-priority', 'due_date', 'created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
            self.progress = 100
        elif self.status != 'completed':
            self.completed_at = None
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.due_date and self.status != 'completed':
            return self.due_date < timezone.now()
        return False
