"""Chat API URLs."""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import ChatSessionViewSet, ChatMessageViewSet

app_name = 'chat_api'

router = DefaultRouter()
router.register('sessions', ChatSessionViewSet, basename='chat-session')
router.register('messages', ChatMessageViewSet, basename='chat-message')

urlpatterns = router.urls
