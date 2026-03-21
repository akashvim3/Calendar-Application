"""
Email app UI views.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Email, EmailAccount


class EmailListView(LoginRequiredMixin, ListView):
    """Main email management UI."""
    model = Email
    template_name = 'email_app/email_list.html'
    context_object_name = 'emails'
    paginate_by = 20

    def get_queryset(self):
        return Email.objects.filter(user=self.request.user, folder='inbox').order_by('-received_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = EmailAccount.objects.filter(user=self.request.user).first()
        return context
