#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyberguard_django.settings')
django.setup()

from django.contrib.auth.models import User
from user_auth.models import UserProfile

def create_missing_profiles():
    """Create UserProfile for users that don't have one"""
    users_without_profile = []
    
    for user in User.objects.all():
        try:
            # Try to get the user profile
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            # Create profile if it doesn't exist
            UserProfile.objects.create(user=user)
            users_without_profile.append(user.username)
            print(f"Created profile for user: {user.username}")
    
    if users_without_profile:
        print(f"\nCreated profiles for {len(users_without_profile)} users: {', '.join(users_without_profile)}")
    else:
        print("All users already have profiles!")

if __name__ == '__main__':
    create_missing_profiles() 