"""Tasks API URLs."""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import TaskViewSet, TaskCategoryViewSet

app_name = 'tasks_api'

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('categories', TaskCategoryViewSet, basename='task-category')

urlpatterns = router.urls
