import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.user_manager import CustomUserManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=300, unique=True, verbose_name="Email address")
    fcm_token = models.CharField(null=True, max_length=128)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
