
from .models import User


class UserFactory:
    @staticmethod
    def create_user(email, username, password=None, **extra_fields):
        return User.objects.create_user(email, username, password, **extra_fields)

    @staticmethod
    def create_superuser(email, username, password=None, **extra_fields):
        return User.objects.create_superuser(email, username, password, **extra_fields)
