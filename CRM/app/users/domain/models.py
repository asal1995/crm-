import hashlib
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from CRM.app.users.infrastructure.models import UserManager

from django.contrib.auth.models import AbstractUser


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    document_hash = models.CharField(max_length=64, blank=True)  # For storing SHA-256 hash
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_created=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    # Add a unique related_name for the user_permissions field
    user_permissions = models.ManyToManyField(
        'auth.Permission',

        related_name='%(class)s_user_permissions',  # Use a unique related_name
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name="user",
    )

    def save(self, *args, **kwargs):
        if self.document:
            self.document_hash = self.generate_document_hash()
        super().save(*args, **kwargs)

    def generate_document_hash(self):
        hasher = hashlib.sha256()
        if self.document and hasattr(self.document, 'file'):
            for chunk in self.document.chunks():
                hasher.update(chunk)
        return hasher.hexdigest()

    def __str__(self):
        return self.email
