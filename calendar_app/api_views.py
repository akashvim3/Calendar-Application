"""
Calendar REST API views.
"""

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, EventCategory
from .serializers import EventSerializer, EventCategorySerializer


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on events."""
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events."""
        from django.utils import timezone
        events = self.get_queryset().filter(
            start_time__gte=timezone.now()
        ).order_by('start_time')[:10]
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's events."""
        from django.utils import timezone
        today = timezone.now().date()
        events = self.get_queryset().filter(
            start_time__date=today
        ).order_by('start_time')
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


class EventCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for event categories."""
    serializer_class = EventCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EventCategory.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
