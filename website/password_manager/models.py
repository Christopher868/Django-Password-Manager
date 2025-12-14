from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
# Model for storing user's saved accounts
class SavedAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_title = models.CharField(max_length=256)
    username_or_email = models.CharField(max_length=255)
    encrypted_password = models.CharField(max_length=256)
    iv = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_title

# Model for storing user's salt
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salt = models.CharField(max_length=255)
    iterations = models.IntegerField()
    iv = models.CharField(max_length=255)
    cipher_text = models.CharField( max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username