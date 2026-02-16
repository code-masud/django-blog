
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Company, Profile

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
    profile = Profile.objects.get(user=instance)

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
