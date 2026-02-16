from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="company_logos/")
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name