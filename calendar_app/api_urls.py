"""Calendar API URLs for REST framework."""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import EventViewSet, EventCategoryViewSet

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('categories', EventCategoryViewSet, basename='event-category')

urlpatterns = router.urls
