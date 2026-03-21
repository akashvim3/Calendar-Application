"""AI core app URLs."""

from django.urls import path
from . import api_views

app_name = 'ai_core'

urlpatterns = [
    path('chat/', api_views.GeminiChatView.as_view(), name='ai-chat'),
    path('detect-intent/', api_views.IntentDetectionView.as_view(), name='ai-detect-intent'),
]
