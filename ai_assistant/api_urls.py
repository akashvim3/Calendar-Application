"""
API URL configuration - Version 1.
All REST API endpoints are consolidated here.
"""

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App APIs
    path('calendar/', include('calendar_app.api_urls')),
    path('tasks/', include('tasks_app.api_urls')),
    path('email/', include('email_app.api_urls')),
    path('chat/', include('chat_app.api_urls')),
    path('notifications/', include('notifications.api_urls')),
    path('ai/', include('ai_core.api_urls')),
]
