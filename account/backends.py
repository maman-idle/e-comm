from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Customer


class CustomUserBackend:
    def authenticate(self, username=None, password=None):
        try:
            user = Customer.objects.get(username=username)
            if check_password(password, user.password):
                return user
            else:
                return None

        except Customer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None
