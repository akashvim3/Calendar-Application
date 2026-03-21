"""Calendar app forms."""

from django import forms
from .models import Event, EventCategory


class EventForm(forms.ModelForm):
    """Form for creating/editing events."""
    
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'location', 'start_time', 'end_time',
            'all_day', 'category', 'priority', 'color', 'recurrence',
            'reminder_minutes', 'meeting_link',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'color': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-input'}),
        }
