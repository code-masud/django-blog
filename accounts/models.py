from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from services.upload_path import logo_upload_path, avatar_upload_path
from services.image_validator import image_validation

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to=logo_upload_path, blank=True, null=True, validators=[image_validation])
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True, validators=[image_validation])
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
