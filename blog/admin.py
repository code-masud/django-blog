from django.contrib import admin
from django.db.models.query import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest
from .models import Category, Tag, Comment, Post
from django.utils import timezone
from django.utils.html import format_html

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ['id', 'preview_image', 'title', 'status', 'created_by', 'created_at', 'updated_by', 'updated_at', 'is_deleted', 'deleted_by', 'deleted_at']
    list_display_links = ['id', 'title']
    list_filter = ['published_at', 'status']
    list_per_page = 10
    search_fields = ['title', 'slug', 'content']
    filter_horizontal = ['categories', 'tags']
    ordering = ['-published_at']

    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author', 'created_by', 'updated_by', 'deleted_by')
    date_hierarchy = 'published_at'
    readonly_fields = ('created_at', 'updated_at')
    actions = ['published_posts', 'restore_posts']

    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Label Specifications', {
            'fields': ('substrate', 'printing_technology', 'finishing_techniques'),
            'classes': ('collapse',)
        }),
        ('Categorization', {
            'fields': ('categories', 'tags')
        }),
        ('Publication Settings', {
            'fields': ('author', 'published_at',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Soft Delete',{
            'fields': ('created_at', 'created_by', 'updated_at', 'updated_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return Post.all_objects.all()

    def preview_image(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src={} style="width:50px;height=50px;">',
                obj.featured_image.url
            )
        return '--'
    preview_image.short_description = 'Image'

    def published_posts(self, request, queryset):
        queryset.update(status=Post.Status.PUBLISHED)
    published_posts.short_description = 'Published selected Posts'

    def restore_posts(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None, deleted_by=None)
    restore_posts.short_description = 'Restore selected Posts'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        obj.delete(user=request.user)
    
    def delete_queryset(self, request: HttpRequest, queryset: QuerySet) -> None:
        for obj in queryset:
            obj.delete(user=request.user)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ['id', 'name', 'slug', 'description', 'is_active']
    list_display_links = ['id', 'name']
    list_filter = ['is_active']
    list_per_page = 10
    search_fields = ['name', 'slug', 'description']
    ordering = ['name']

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Main Content', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        obj.delete(user=request.user)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag

    list_display = ['id', 'name', 'slug', 'description', 'is_active']
    list_display_links = ['id', 'name']
    list_filter = ['is_active']
    list_per_page = 10
    search_fields = ['name', 'slug', 'description']
    ordering = ['name']

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Main Content', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        obj.delete(user=request.user)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment

    list_display = ['id', 'short_text', 'post', 'user', 'is_approved']
    list_display_links = ['id', 'post']
    list_filter = ['is_approved']
    list_per_page = 10
    search_fields = ['post__title', 'user__username', 'text']
    ordering = ['post']
    actions = ['approve_comments']

    fieldsets = (
        ('Main Content', {
            'fields': ('post', 'user', 'text', 'is_approved')
        }),
    )

    def short_text(self, obj):
        return obj.text[:10] + '...' if len(obj.text) > 10 else obj.text
    short_text.short_description = 'Comment'

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Approve selected comments'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        obj.delete(user=request.user)