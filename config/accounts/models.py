from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # You can add extra fields here if needed
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username



class VulnUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # Stored in plain text!

    def __str__(self):
        return self.username
