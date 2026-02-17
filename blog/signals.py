from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Post

def delete_file(file=None):
    if not file:
        return
    
    if default_storage.exists(file.name):
        default_storage.delete(file.name)

@receiver(pre_save, sender=Post)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    old_obj = get_object_or_404(Post, pk=instance.pk)
    if old_obj.featured_image and old_obj.featured_image != instance.featured_image:
        delete_file(old_obj.featured_image)

@receiver(post_delete, sender=Post)
def delete_image_on_delete(sender, instance, **kwargs):
    delete_file(getattr(instance,'featured_image', None))