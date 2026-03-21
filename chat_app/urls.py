"""Chat app URLs."""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import ChatSessionViewSet, ChatMessageViewSet
from . import views

app_name = 'chat_app'

# API Routes
router = DefaultRouter()
router.register('sessions', ChatSessionViewSet, basename='chat-session')
router.register('messages', ChatMessageViewSet, basename='chat-message')

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat'),
    path('session/<str:session_id>/', views.ChatSessionView.as_view(), name='chat-session'),
] + router.urls
