from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from .models import Category, Tag, Comment, Post
from django.utils import timezone

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ['id', 'title', 'slug', 'featured_image', 'status']
    list_display_links = ['id', 'title']
    list_filter = ['published_at', 'status']
    list_per_page = 10
    search_fields = ['title', 'slug', 'content']
    filter_horizontal = ['categories', 'tags']
    ordering = ['-published_at']

    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_at'

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
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            self.author = request.user
            self.created_by = request.user
        else:
            self.updated_by = request.user
        return super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
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
            self.created_by = request.user
        else:
            self.updated_by = request.user
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
            self.created_by = request.user
        else:
            self.updated_by = request.user
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
            self.created_by = request.user
        else:
            self.updated_by = request.user
        return super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        obj.delete(user=request.user)