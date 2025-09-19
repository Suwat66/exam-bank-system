from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        TEACHER = 'TEACHER', 'Teacher'

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.TEACHER)
    is_approved = models.BooleanField(default=False, help_text="Designates whether the teacher is approved by an admin.")