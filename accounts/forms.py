from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from .models import Contact
from allauth.account.forms import SignupForm
from .models import Profile

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    avatar = forms.ImageField()
    phone = PhoneNumberField()
    address = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")

        # Check email already exists in Profile
        if email and Profile.objects.filter(email=email).exists():
            self.add_error("email", "This email is already registered.")

        # Check phone already exists
        if phone and Profile.objects.filter(phone=phone).exists():
            self.add_error("phone", "This phone number is already registered.")

        return cleaned_data
    
    def save(self, request):
        user = super().save(request)

        avatar = self.cleaned_data.get('avatar')
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'email':user.email,
                'name':user.get_full_name(),
                'phone':self.cleaned_data['phone'],
                'avatar':avatar,
                'address':self.cleaned_data['address'],
            }
        )
        return user
    
    # def signup(self, request, user):
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.save()

    #     avatar = self.cleaned_data.get('avatar')
    #     Profile.objects.update_or_create(
    #         user=user,
    #         defaults={
    #             'email':user.email,
    #             'name':user.get_full_name,
    #             'phone':self.cleaned_data['phone'],
    #             'avatar':avatar,
    #             'address':self.cleaned_data['address'],
    #         }
    #     )

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'message']

# class CustomUserCreationForm(UserCreationForm):
#     avatar = forms.ImageField()
#     phone = PhoneNumberField()
#     address = forms.Textarea()

#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'password',
#             'first_name',
#             'last_name',
#             'email',
#         ]