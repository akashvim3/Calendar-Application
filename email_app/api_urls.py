"""Email API URLs."""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import EmailViewSet, EmailAccountViewSet

app_name = 'email_api'

router = DefaultRouter()
router.register('emails', EmailViewSet, basename='email')
router.register('accounts', EmailAccountViewSet, basename='email-account')

urlpatterns = router.urls
