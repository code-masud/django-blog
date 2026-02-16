from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from services.image_validator import image_validation
from services.upload_path import post_upload_path
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import transaction
from django.core.validators import MinLengthValidator

class SoftDeleteQuerySet(models.QuerySet):

    def delete(self, user=None):
        update_data = {
            "is_deleted": True,
            "deleted_at": timezone.now(),
        }

        if user and isinstance(user, User):
            update_data["deleted_by"] = user

        return super().update(**update_data)

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return super().update(
            is_deleted=False,
            deleted_at=None,
            deleted_by=None,
        )

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def dead(self):
        return self.get_queryset().dead()


class SoftDeleteMixin(models.Model):

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )

    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_deleted",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    @transaction.atomic
    def delete(self, using=None, keep_parents=False, user=None):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    @transaction.atomic
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])

class Category(SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    slug = models.SlugField(max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(help_text='Short description')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'slug'], condition=Q(is_active=True), name='category_unique_name_slug')
        ]
        indexes = [
            models.Index(fields=['is_active', 'name']),
            models.Index(fields=['is_active', 'slug'])
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Tag(SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    slug = models.SlugField(max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(help_text='Short description')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'slug'], condition=Q(is_active=True), name='tag_unique_name_slug')
        ]
        indexes = [
            models.Index(fields=['is_active', 'name']),
            models.Index(fields=['is_active', 'slug'])
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
class Post(SoftDeleteMixin, models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PB', 'Published'
        ARCHIVE = 'AR', 'Archive'
    
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    slug = models.SlugField(max_length=200, validators=[MinLengthValidator(5)])
    excerpt = models.TextField(help_text="Brief summary for listings", max_length=300)
    content = models.TextField()
    featured_image = models.ImageField(upload_to=post_upload_path, blank=True, null=True, validators=[image_validation])
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    # Technical specifications for label projects
    substrate = models.CharField(max_length=100, blank=True, help_text="Label material")
    printing_technology = models.CharField(max_length=100, blank=True)
    finishing_techniques = models.CharField(max_length=200, blank=True)

    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    published_at = models.DateTimeField(blank=True, null=True)

    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['-published_at']
        constraints = [
            models.UniqueConstraint(fields=['title', 'slug'], condition=Q(status='PB'), name='post_unique_name_slug')
        ]
        indexes = [
            models.Index(fields=['status', 'title']),
            models.Index(fields=['status', 'slug'])
        ]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("blog:post_detail", args=[self.slug])
    
class Comment(SoftDeleteMixin, models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='blog_comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    is_approved = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'