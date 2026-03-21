"""Notifications app URLs."""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import NotificationViewSet

app_name = 'notifications_api'

# API Routes
router = DefaultRouter()
router.register('notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # API endpoints
] + router.urls
