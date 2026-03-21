"""
Forms for notifications app.
"""

from django import forms
from accounts.models import User


class NotificationPreferencesForm(forms.ModelForm):
    """Form for managing user notification preferences."""
    
    class Meta:
        model = User
        fields = ['email_notifications', 'push_notifications', 'daily_briefing']
        widgets = {
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'push_notifications': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'daily_briefing': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }