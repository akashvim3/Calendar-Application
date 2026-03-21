"""
Account views for registration, login, profile management.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, ForgotPasswordForm, ResetPasswordForm, ChangePasswordForm


class RegisterView(View):
    """User registration view."""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created successfully.')
            return redirect('dashboard:home')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    """User login view."""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.display_name}!')
                next_url = request.GET.get('next', 'dashboard:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    """User logout view."""
    
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('home')


class ProfileView(LoginRequiredMixin, View):
    """User profile view."""
    
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form})
    
    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        return render(request, 'accounts/profile.html', {'form': form})


class SettingsView(LoginRequiredMixin, View):
    """User settings view."""
    
    def get(self, request):
        return render(request, 'accounts/settings.html')
    
    def post(self, request):
        user = request.user
        user.theme = request.POST.get('theme', 'dark')
        user.email_notifications = request.POST.get('email_notifications') == 'on'
        user.push_notifications = request.POST.get('push_notifications') == 'on'
        user.daily_briefing = request.POST.get('daily_briefing') == 'on'
        user.ai_suggestions_enabled = request.POST.get('ai_suggestions') == 'on'
        user.voice_assistant_enabled = request.POST.get('voice_assistant') == 'on'
        user.preferred_timezone = request.POST.get('timezone', 'Asia/Kolkata')
        user.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('accounts:settings')


class IntegrationsView(LoginRequiredMixin, View):
    """User integrations view for connecting third-party apps."""
    
    def get(self, request):
        return render(request, 'accounts/integrations.html')


class ForgotPasswordView(View):
    """Forgot password view."""
    
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'accounts/forgot_password.html', {'form': form})
    
    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Build reset URL
                reset_url = request.build_absolute_uri(
                    reverse('accounts:reset_password_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                
                # Send email
                subject = 'Password Reset Request'
                message = render_to_string('accounts/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                
                messages.success(request, 'If an account with that email exists, we have sent you a password reset link.')
                return redirect('accounts:forgot_password')
            except User.DoesNotExist:
                # Don't reveal that the email doesn't exist for security
                messages.success(request, 'If an account with that email exists, we have sent you a password reset link.')
                return redirect('accounts:forgot_password')
        return render(request, 'accounts/forgot_password.html', {'form': form})


class ResetPasswordConfirmView(View):
    """Reset password confirmation view."""
    
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            form = ResetPasswordForm()
            return render(request, 'accounts/reset_password_confirm.html', {
                'form': form,
                'uidb64': uidb64,
                'token': token
            })
        else:
            messages.error(request, 'The password reset link is invalid or has expired.')
            return redirect('accounts:forgot_password')
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['new_password1']
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password has been reset successfully. You can now log in.')
                return redirect('accounts:login')
        else:
            messages.error(request, 'The password reset link is invalid or has expired.')
            return redirect('accounts:forgot_password')
        
        return render(request, 'accounts/reset_password_confirm.html', {
            'form': form,
            'uidb64': uidb64,
            'token': token
        })


class ChangePasswordView(LoginRequiredMixin, View):
    """Change password view."""
    
    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'accounts/change_password.html', {'form': form})
    
    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password1']
            
            # Check if current password is correct
            if request.user.check_password(current_password):
                request.user.set_password(new_password)
                request.user.save()
                # Update session to prevent logout
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('accounts:settings')
            else:
                form.add_error('current_password', 'Your current password is incorrect.')
        return render(request, 'accounts/change_password.html', {'form': form})


class DeactivateAccountView(LoginRequiredMixin, View):
    """Deactivate account view with confirmation."""
    
    def get(self, request):
        return render(request, 'accounts/deactivate.html')
    
    def post(self, request):
        # Soft delete user account
        user = request.user
        user.is_active = False
        user.save()
        
        # Logout user
        logout(request)
        messages.success(request, 'Your account has been deactivated. You can reactivate it by logging in.')
        return redirect('home')
