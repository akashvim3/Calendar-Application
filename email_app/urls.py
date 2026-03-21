"""Email app URLs."""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import EmailViewSet, EmailAccountViewSet

from . import views

app_name = 'email_app'

# API Routes
router = DefaultRouter()
router.register('emails', EmailViewSet, basename='email')
router.register('accounts', EmailAccountViewSet, basename='email-account')

urlpatterns = [
    path('', views.EmailListView.as_view(), name='email-list'),
] + router.urls
