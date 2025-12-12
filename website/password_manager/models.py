from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class SavedAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    encrypted_username_or_email = models.TextField()
    encrypted_password = models.TextField()
    key_salt = models.CharField(max_length=256)
    iv = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
