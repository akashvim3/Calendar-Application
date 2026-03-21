"""Calendar serializers for REST API."""

from rest_framework import serializers
from .models import Event, EventCategory


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'color', 'icon']


class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    duration_minutes = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'location', 'start_time', 'end_time',
            'all_day', 'timezone', 'category', 'category_name', 'priority',
            'color', 'recurrence', 'recurrence_end', 'reminder_minutes',
            'meeting_link', 'meeting_notes', 'duration_minutes', 'is_past',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
