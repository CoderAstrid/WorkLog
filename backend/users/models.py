from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Role field is now part of CustomUser instead of using a Profile model
    ROLE_CHOICES = [('admin', 'Admin'), ('user', 'User')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # Resolve conflict by specifying unique related_name
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
