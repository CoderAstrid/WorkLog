from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

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

    security_question_1 = models.CharField(max_length=255, blank=True, null=True)
    security_answer_1 = models.CharField(max_length=255, blank=True, null=True)
    security_question_2 = models.CharField(max_length=255, blank=True, null=True)
    security_answer_2 = models.CharField(max_length=255, blank=True, null=True)
    security_question_3 = models.CharField(max_length=255, blank=True, null=True)
    security_answer_3 = models.CharField(max_length=255, blank=True, null=True)

    failed_attempts = models.IntegerField(default=0)  # Track failed attempts
    lock_until = models.DateTimeField(blank=True, null=True)  # Lock time
    
    def save(self, *args, **kwargs):
        # Ensure only up to 2 admin users exist
        if self.is_staff and CustomUser.objects.filter(is_staff=True).count() >= 2:
            raise ValidationError("Only two admin accounts are allowed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} (Admin)" if self.is_staff else f"{self.username} (User)"
