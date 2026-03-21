"""Calendar app URLs."""

from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('events/', views.EventListAPIView.as_view(), name='event_list'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
]
