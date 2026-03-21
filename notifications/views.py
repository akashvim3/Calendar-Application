"""
Notifications UI views.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Notification
from .forms import NotificationPreferencesForm


class NotificationListView(LoginRequiredMixin, ListView):
    """Notification management UI."""
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class NotificationPreferencesView(LoginRequiredMixin, TemplateView):
    """Notification preferences management."""
    template_name = 'notifications/preferences.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NotificationPreferencesForm(instance=self.request.user)
        return context

    def post(self, request):
        form = NotificationPreferencesForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification preferences updated successfully!')
            return redirect('notifications:preferences')
        return render(request, self.template_name, {'form': form})
