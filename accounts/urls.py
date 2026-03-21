"""Account URLs."""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('integrations/', views.IntegrationsView.as_view(), name='integrations'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('deactivate/', views.DeactivateAccountView.as_view(), name='deactivate'),
]
