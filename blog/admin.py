
from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from .models import Category, Tag, Comment, Post
from django.utils.html import format_html
from config.admin import AuditAdminMixin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages

@admin.register(Post)
class PostAdmin(AuditAdminMixin, admin.ModelAdmin):
    model = Post

    list_display = ('id', 'preview_image', 'title', 'status', 'restore_button',)
    list_display_links = ('id', 'title')
    list_filter = ('published_at', 'status')
    list_per_page = 10
    search_fields = ('title', 'slug', 'content')
    filter_horizontal = ('categories', 'tags')
    ordering = ('-published_at',)

    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author', 'created_by', 'updated_by', 'deleted_by')
    date_hierarchy = 'published_at'
    actions = ('published_posts', )

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

    @admin.display(description='Image')
    def preview_image(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src={} style="width:50px;height=50px;">',
                obj.featured_image.url
            )
        return '--'
    
    @admin.action(description='Published selected Posts')
    def published_posts(self, request, queryset):
        qs = queryset.exclude(status=Post.Status.PUBLISHED)
        count = qs.update(status=Post.Status.PUBLISHED)
        self.message_user(request, f'{count} posts status updated successfully.')
    
@admin.register(Category)
class CategoryAdmin(AuditAdminMixin, admin.ModelAdmin):
    model = Category

    list_display = ('id', 'name', 'slug', 'description', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('is_active',)
    list_per_page = 10
    search_fields = ('name', 'slug', 'description')
    ordering = ('name',)

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Main Content', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('Soft Delete',{
            'fields': ('created_at', 'created_by', 'updated_at', 'updated_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        })
    )

@admin.register(Tag)
class TagAdmin(AuditAdminMixin, admin.ModelAdmin):
    model = Tag

    list_display = ('id', 'name', 'slug', 'description', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('is_active',)
    list_per_page = 10
    search_fields = ('name', 'slug', 'description')
    ordering = ('name',)

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Main Content', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('Soft Delete',{
            'fields': ('created_at', 'created_by', 'updated_at', 'updated_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        })
    )

@admin.register(Comment)
class CommentAdmin(AuditAdminMixin, admin.ModelAdmin):
    model = Comment

    list_display = ('id', 'short_text', 'post', 'user', 'is_approved')
    list_display_links = ('id', 'post')
    list_filter = ('is_approved',)
    list_per_page = 10
    search_fields = ('post__title', 'user__username', 'text')
    ordering = ('post',)
    actions = ('approve_comments',)

    fieldsets = (
        ('Main Content', {
            'fields': ('post', 'user', 'text', 'is_approved')
        }),
        ('Soft Delete',{
            'fields': ('created_at', 'created_by', 'updated_at', 'updated_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        })
    )

    @admin.display(description='Comment')
    def short_text(self, obj):
        return obj.text[:10] + '...' if len(obj.text) > 10 else obj.text

    @admin.display(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)