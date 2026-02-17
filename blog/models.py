from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from services.image_validator import image_validation
from services.upload_path import article_upload_path
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.validators import MinLengthValidator
from config.models.mixins import AuditSoftDeleteMixin as SoftDeleteMixin
from config.models.mixins import SEOMixin

class Category(SoftDeleteMixin, SEOMixin, models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    slug = models.SlugField(max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(help_text='Short description')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'slug'], condition=Q(is_active=True), name='%(app_label)s_%(class)s_unique_name_slug')
        ]
        indexes = [
            models.Index(fields=['is_active', 'name']),
            models.Index(fields=['is_active', 'slug'])
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy("blog:category_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Tag(SoftDeleteMixin, SEOMixin, models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    slug = models.SlugField(max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(help_text='Short description')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'slug'], condition=Q(is_active=True), name='%(app_label)s_%(class)s_unique_name_slug')
        ]
        indexes = [
            models.Index(fields=['is_active', 'name']),
            models.Index(fields=['is_active', 'slug'])
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy("blog:tag_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
class Article(SoftDeleteMixin, SEOMixin, models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PB', 'Published'
        ARCHIVE = 'AR', 'Archive'
    
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    slug = models.SlugField(max_length=200, validators=[MinLengthValidator(5)])
    content = models.TextField()
    featured_image = models.ImageField(upload_to=article_upload_path, blank=True, null=True, validators=[image_validation])
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    categories = models.ManyToManyField(Category, related_name='articles', blank=True)
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)

    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    published_at = models.DateTimeField(blank=True, null=True)

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Articles'
        ordering = ['-published_at']
        constraints = [
            models.UniqueConstraint(fields=['title', 'slug'], condition=Q(status='PB'), name='%(app_label)s_%(class)s_unique_name_slug'),
            models.CheckConstraint(check=Q(views__gte=0, likes__gte=0), name="%(app_label)s_%(class)s_stats_positive"),
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
        return reverse_lazy("blog:article_detail", args=[self.slug])
    
class Comment(SoftDeleteMixin, models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='blog_comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    is_approved = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'