"""
Calendar views for event management UI.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
import json
from .models import Event, EventCategory
from .forms import EventForm


class CalendarView(LoginRequiredMixin, View):
    """Main calendar page with full calendar UI."""
    
    def get(self, request):
        categories = EventCategory.objects.filter(user=request.user)
        # Create default categories if none exist
        if not categories.exists():
            defaults = [
                {'name': 'Work', 'color': '#6366f1', 'icon': 'briefcase'},
                {'name': 'Personal', 'color': '#10b981', 'icon': 'user'},
                {'name': 'Meeting', 'color': '#f59e0b', 'icon': 'users'},
                {'name': 'Health', 'color': '#ef4444', 'icon': 'heart'},
            ]
            for cat_data in defaults:
                EventCategory.objects.create(user=request.user, **cat_data)
            categories = EventCategory.objects.filter(user=request.user)
        
        return render(request, 'calendar_app/calendar.html', {
            'categories': categories,
        })


class EventListAPIView(LoginRequiredMixin, View):
    """API endpoint for fetching events (used by FullCalendar JS)."""
    
    def get(self, request):
        start = request.GET.get('start')
        end = request.GET.get('end')
        
        events = Event.objects.filter(
            user=request.user,
            is_active=True,
        )
        
        if start:
            events = events.filter(start_time__gte=start)
        if end:
            events = events.filter(end_time__lte=end)
        
        event_list = []
        for event in events:
            event_list.append({
                'id': event.id,
                'title': event.title,
                'start': event.start_time.isoformat(),
                'end': event.end_time.isoformat(),
                'color': event.color or (event.category.color if event.category else '#6366f1'),
                'allDay': event.all_day,
                'extendedProps': {
                    'description': event.description,
                    'location': event.location,
                    'category': event.category.name if event.category else '',
                    'priority': event.priority,
                    'meeting_link': event.meeting_link,
                },
            })
        
        return JsonResponse(event_list, safe=False)


class EventCreateView(LoginRequiredMixin, View):
    """Create a new event."""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST
        
        category = None
        category_id = data.get('category')
        if category_id:
            category = EventCategory.objects.filter(id=category_id, user=request.user).first()
        
        event = Event.objects.create(
            user=request.user,
            title=data.get('title', 'New Event'),
            description=data.get('description', ''),
            location=data.get('location', ''),
            start_time=data.get('start_time') or data.get('start'),
            end_time=data.get('end_time') or data.get('end'),
            all_day=data.get('all_day', False),
            category=category,
            priority=data.get('priority', 'medium'),
            color=data.get('color', category.color if category else '#6366f1'),
            recurrence=data.get('recurrence', 'none'),
            reminder_minutes=int(data.get('reminder_minutes', 30)),
            meeting_link=data.get('meeting_link', ''),
        )
        
        return JsonResponse({
            'status': 'success',
            'event': {
                'id': event.id,
                'title': event.title,
                'start': event.start_time.isoformat(),
                'end': event.end_time.isoformat(),
                'color': event.color,
            }
        })


class EventUpdateView(LoginRequiredMixin, View):
    """Update an existing event."""
    
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk, user=request.user)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST
        
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.location = data.get('location', event.location)
        
        if data.get('start_time') or data.get('start'):
            event.start_time = data.get('start_time') or data.get('start')
        if data.get('end_time') or data.get('end'):
            event.end_time = data.get('end_time') or data.get('end')
        
        event.all_day = data.get('all_day', event.all_day)
        event.priority = data.get('priority', event.priority)
        event.color = data.get('color', event.color)
        event.meeting_link = data.get('meeting_link', event.meeting_link)
        event.save()
        
        return JsonResponse({'status': 'success'})


class EventDeleteView(LoginRequiredMixin, View):
    """Delete an event."""
    
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk, user=request.user)
        event.delete()
        return JsonResponse({'status': 'success'})
