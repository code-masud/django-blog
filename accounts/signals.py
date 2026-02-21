
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Company, Profile
from allauth.socialaccount.signals import social_account_added
from django.core.files.base import ContentFile

@receiver(social_account_added)
def on_social_account_added(request, sociallogin, **kwargs):
    print(sociallogin)
    if sociallogin.account.provider == 'google':
        user = sociallogin.user
        picture_url = sociallogin.account.extra_data.get('picture')

        if not picture_url:
            return
        
        profile, created = Profile.objects.get_or_create(user=user)

        if profile.avatar:
            return
        
        response = request.get(picture_url)
        if response.status_code == 200:
            profile.avatar.save(
                f"{user.username}_google.jpg",
                ContentFile(response.content),
                save=True
            )

def delete_file(file=None):
    if not file:
        return
    
    if default_storage.exists(file.name):
        default_storage.delete(file.name)

# Company
@receiver(pre_save, sender=Company)
def remove_old_logo_on_change(sender, instance, **kwargs):
    if not instance.id:
        return
    
    old_obj = get_object_or_404(Company,pk=instance.id)
    if old_obj.logo and instance.logo != old_obj.logo:
        delete_file(old_obj.logo)

@receiver(post_delete, sender=Company)
def remove_logo_on_delete(sender, instance, **kwargs):
    delete_file(getattr(instance, 'logo'))

# User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    Profile.objects.update_or_create(
        user=instance,
        defaults={'email':instance.email, 'name':instance.get_full_name}
    )

@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    profile = Profile.objects.filter(user=instance).first()

    if profile:
        if profile.avatar:
            delete_file(profile.avatar)
        profile.delete()

# Profile
@receiver(pre_save, sender=Profile)
def remove_old_avatar(sender, instance, **kwargs):
    if not instance.id:
        return
    
    old_obj = get_object_or_404(Profile, pk=instance.id)
    if old_obj.avatar and old_obj.avatar != instance.avatar:
        delete_file(old_obj.avatar)

@receiver(post_delete, sender=Profile)
def remove_profile_avatar(sender, instance, **kwargs):
    delete_file(getattr(instance, 'avatar'))
