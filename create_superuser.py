import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_assistant.settings')
django.setup()

from accounts.models import User

username = 'admin'
email = 'admin@example.com'
password = 'adminpassword123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")
