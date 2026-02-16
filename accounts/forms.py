from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

class CustomUserCreationForm(UserCreationForm):
    avatar = forms.ImageField()
    phone = PhoneNumberField()
    address = forms.Textarea()

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'avatar',
            'phone',
            'email',
            'address'
        ]