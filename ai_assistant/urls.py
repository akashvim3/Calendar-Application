"""
Main URL configuration for AI Personal Assistant.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import HomeView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # App URLs
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('calendar/', include('calendar_app.urls', namespace='calendar_app')),
    path('email/', include('email_app.urls', namespace='email_app')),
    path('tasks/', include('tasks_app.urls', namespace='tasks_app')),
    path('chat/', include('chat_app.urls', namespace='chat_app')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    
    # API URLs
    path('api/v1/', include('ai_assistant.api_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
