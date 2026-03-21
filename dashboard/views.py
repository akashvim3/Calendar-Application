"""
Dashboard views for central application UI.
Aggregates data from all apps to show a daily summary.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from datetime import timedelta
from calendar_app.models import Event
from tasks_app.models import Task
from email_app.models import Email
from notifications.models import Notification


class HomeView(View):
    """Public landing page view."""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, 'landing.html')


class DashboardView(LoginRequiredMixin, View):
    """Main dashboard summary view."""
    
    def get(self, request):
        now = timezone.now()
        today = now.date()
        
        # 1. Today's Events
        events_today = Event.objects.filter(
            user=request.user,
            start_time__date=today,
            is_active=True
        ).order_by('start_time')
        
        # 2. Pending Tasks
        pending_tasks = Task.objects.filter(
            user=request.user,
            status__in=['todo', 'in_progress']
        ).order_by('due_date', '-priority')[:5]
        
        # 3. Important Emails (Unread)
        recent_emails = Email.objects.filter(
            user=request.user,
            folder='inbox',
            is_read=False
        ).order_by('-received_at')[:5]
        
        # 4. Notifications
        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).order_by('-created_at')[:5]
        
        # 5. Productivity Stats
        completed_tasks_today = Task.objects.filter(
            user=request.user,
            status='completed',
            completed_at__date=today
        ).count()
        
        total_tasks_today = Task.objects.filter(
            user=request.user,
            due_date__date=today
        ).count()
        
        productivity_score = 0
        if total_tasks_today > 0:
            productivity_score = int((completed_tasks_today / total_tasks_today) * 100)
            
        context = {
            'events_today': events_today,
            'pending_tasks': pending_tasks,
            'recent_emails': recent_emails,
            'unread_notifications': unread_notifications,
            'productivity_score': productivity_score,
            'completed_tasks_today': completed_tasks_today,
            'total_tasks_today': total_tasks_today,
            'ai_greeting': self.get_ai_greeting(request.user),
        }
        
        return render(request, 'dashboard/index.html', context)

    def get_ai_greeting(self, user):
        """Simple rule-based greeting before full AI integration."""
        from django.utils import timezone
        hour = timezone.now().hour
        
        if hour < 12:
            base = "Good morning"
        elif hour < 18:
            base = "Good afternoon"
        else:
            base = "Good evening"
            
        return f"{base}, {user.first_name or user.username}. "

