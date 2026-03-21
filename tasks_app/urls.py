"""Tasks app URLs."""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import TaskViewSet, TaskCategoryViewSet

from . import views

app_name = 'tasks_app'

# API Routes
router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('categories', TaskCategoryViewSet, basename='task-category')

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
] + router.urls
