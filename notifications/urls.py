"""Notifications app UI URLs."""

from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('preferences/', views.NotificationPreferencesView.as_view(), name='preferences'),
]
