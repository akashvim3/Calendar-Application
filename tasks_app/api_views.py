"""
Tasks REST API views.
"""

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Task, TaskCategory
from .serializers import TaskSerializer, TaskCategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on tasks."""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'status', 'created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary stats for tasks."""
        queryset = self.get_queryset()
        return Response({
            'total': queryset.count(),
            'todo': queryset.filter(status='todo').count(),
            'in_progress': queryset.filter(status='in_progress').count(),
            'completed': queryset.filter(status='completed').count(),
            'overdue': queryset.filter(due_date__lt=timezone.now(), status__in=['todo', 'in_progress']).count()
        })

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get tasks due today."""
        today = timezone.now().date()
        tasks = self.get_queryset().filter(due_date__date=today).order_by('due_date')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

class TaskCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for task categories."""
    serializer_class = TaskCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
