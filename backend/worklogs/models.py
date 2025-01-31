from django.db import models

# Create your models here.
from users.models import CustomUser

class WorkLog(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define ID
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
