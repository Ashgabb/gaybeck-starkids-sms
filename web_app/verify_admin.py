#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

try:
    user = User.objects.get(email='admin@example.com')
    print(f"✓ User found: {user.email}")
    print(f"  First name: {user.first_name}")
    print(f"  Last name: {user.last_name}")
    print(f"  Is active: {user.is_active}")
    print(f"  Is staff: {user.is_staff}")
    print(f"  Password hash: {user.password[:20]}...")
except User.DoesNotExist:
    print("✗ User not found - creating now...")
    User.objects.create_superuser(
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print("✓ Admin user created successfully")
