"""Tasks app serializers."""

from rest_framework import serializers
from .models import Task, TaskCategory


class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = ['id', 'name', 'color']


class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'priority', 'status',
            'progress', 'category', 'category_name', 'reminder_at', 'is_overdue',
            'created_at', 'updated_at', 'completed_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'completed_at']
