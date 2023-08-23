from django.contrib.auth.backends import ModelBackend
from .models import UserRegistration

class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserRegistration.objects.get(username=username)
            if user.check_password(password):
                return user
        except UserRegistration.DoesNotExist:
            return None
