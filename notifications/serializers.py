"""Notifications app serializers."""

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    time_since = serializers.ReadOnlyField()

    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 'priority',
            'is_read', 'action_url', 'metadata', 'created_at', 'time_since'
        ]
        read_only_fields = ['created_at', 'time_since']
