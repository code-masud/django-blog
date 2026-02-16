from django.contrib import admin
from .models import Category, Tag, Comment, Post


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
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ['id', 'name', 'slug', 'description', 'is_active']
    list_display_links = ['id', 'name']
    list_filter = ['is_active']
    list_per_page = 10
    search_fields = ['name', 'slug', 'description']
    ordering = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag

    list_display = ['id', 'name', 'slug', 'description', 'is_active']
    list_display_links = ['id', 'name']
    list_filter = ['is_active']
    list_per_page = 10
    search_fields = ['name', 'slug', 'description']
    ordering = ['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment

    list_display = ['id', 'post', 'user', 'text', 'is_approved']
    list_display_links = ['id', 'post']
    list_filter = ['is_approved']
    list_per_page = 10
    search_fields = ['post', 'user', 'text']
    ordering = ['post']