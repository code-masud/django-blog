
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from ..managers import AuditSoftDeleteManager
from services.image_validator import image_validation
from services.upload_path import seo_upload_path

class AuditSoftDeleteMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated",
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_deleted",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    alive_objects = AuditSoftDeleteManager()

    class Meta:
        abstract = True

    @transaction.atomic
    def delete(self, using=None, keep_parents=False, user=None):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])

    @transaction.atomic
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)
    
class SEOMixin(models.Model):
    # Meta SEO
    meta_title = models.CharField(max_length=255, blank=True, help_text="Max 255 characters for SEO")
    meta_description = models.TextField(blank=True, help_text="Max 500 characters for SEO")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")
    canonical_url = models.URLField(blank=True, help_text="Leave empty to use default post URL")

    # OpenGraph
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to=seo_upload_path, blank=True, validators=[image_validation])

    # Twitter
    twitter_title = models.CharField(max_length=255, blank=True)
    twitter_description = models.TextField(blank=True)
    twitter_image = models.ImageField(upload_to=seo_upload_path, blank=True, validators=[image_validation])

    class Meta:
        abstract = True