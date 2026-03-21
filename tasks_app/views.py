"""
Tasks app UI views.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Task, TaskCategory


class TaskListView(LoginRequiredMixin, ListView):
    """Main tasks management UI."""
    model = Task
    template_name = 'tasks_app/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-priority', 'due_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TaskCategory.objects.filter(user=self.request.user)
        return context
