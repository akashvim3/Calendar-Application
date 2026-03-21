"""
Chat UI views.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ChatSession


class ChatView(LoginRequiredMixin, ListView):
    """Main chat application UI."""
    model = ChatSession
    template_name = 'chat_app/chat.html'
    context_object_name = 'chat_sessions'
    paginate_by = 10

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user, is_archived=False).order_by('-updated_at')


class ChatSessionView(LoginRequiredMixin, DetailView):
    """Individual chat session view."""
    model = ChatSession
    template_name = 'chat_app/chat.html'
    context_object_name = 'chat_session'
    pk_url_kwarg = 'session_id'
    slug_field = 'session_id'
    slug_url_kwarg = 'session_id'

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_sessions'] = ChatSession.objects.filter(user=self.request.user, is_archived=False).order_by('-updated_at')[:10]
        return context
