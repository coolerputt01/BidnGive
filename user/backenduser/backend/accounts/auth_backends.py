# accounts/auth_backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class InactiveUserAllowedBackend(ModelBackend):
    def user_can_authenticate(self, user):
        """Allow even inactive users to authenticate."""
        return True  # ⚠️ Allow all users, even if inactive
