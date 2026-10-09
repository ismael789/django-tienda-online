import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_online.settings')
django.setup()

from django.contrib.auth.models import User

u = User.objects.get(username='admin')
u.set_password('admin123')
u.save()
print("Password set.")
