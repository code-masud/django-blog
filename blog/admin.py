from django.contrib import admin
from .models import Category, Tag, Comment, Article
from django.utils.html import format_html
from config.admin import AuditAdminMixin
from django.utils import timezone

@admin.register(Article)
class ArticleAdmin(AuditAdminMixin, admin.ModelAdmin):
    model = Article

    list_display = ('id', 'preview_image', 'title', 'status',)
    list_display_links = ('id', 'title')
    list_filter = ('published_at', 'status')
    list_per_page = 10
    search_fields = ('title', 'slug', 'content')
    filter_horizontal = ('categories', 'tags')
    ordering = ('-published_at',)

    seo_fields = ['slug', 'meta_title', 'meta_description', 
          'meta_keywords', 'og_title', 'og_description', 'twitter_title', 'twitter_description']
    
    prepopulated_fields = {field: ('title',) for field in seo_fields}
    raw_id_fields = ('author', 'created_by', 'updated_by', 'deleted_by')
    date_hierarchy = 'published_at'
    actions = ('published_articles', )

    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'slug', 'content', 'featured_image',)
        }),
        ('Categorization', {
            'fields': ('categories', 'tags')
        }),
        ('Publication Settings', {
            'fields': ('status', 'author', 'published_at',)
        }),
        ('Statistics', {
            'fields': ('views', 'likes',),
            'classes': ('collapse',)
        }),
        ('SEO',{
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 'og_title', 'og_description', 'og_image','twitter_title', 'twitter_description', 'twitter_image'),
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
    
    @admin.action(description='Published selected Articles')
    def published_articles(self, request, queryset):
        qs = queryset.exclude(status=Article.Status.PUBLISHED)
        count = qs.update(status=Article.Status.PUBLISHED, published_at=timezone.now())
        self.message_user(request, f'{count} articles published successfully.')
    
@admin.register(Category)
class CategoryAdmin(AuditAdminMixin, admin.ModelAdmin):
    model = Category

    list_display = ('id', 'name', 'slug', 'description', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('is_active',)
    list_per_page = 10
    search_fields = ('name', 'slug', 'description')
    ordering = ('name',)

    seo_fields = ['slug', 'description', 'meta_title', 'meta_description', 
          'meta_keywords', 'og_title', 'og_description', 'twitter_title', 'twitter_description']
    prepopulated_fields = {field: ('name',) for field in seo_fields}

    fieldsets = (
        ('Main Content', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('SEO',{
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 'og_title', 'og_description', 'og_image','twitter_title', 'twitter_description', 'twitter_image'),
            'classes': ('collapse',)
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

    seo_fields = ['slug', 'description', 'meta_title', 'meta_description', 
          'meta_keywords', 'og_title', 'og_description', 'twitter_title', 'twitter_description']
    prepopulated_fields = {field: ('name',) for field in seo_fields}

    fieldsets = (
        ('Main Content', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('SEO',{
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 'og_title', 'og_description', 'og_image','twitter_title', 'twitter_description', 'twitter_image'),
            'classes': ('collapse',)
        }),
        ('Soft Delete',{
            'fields': ('created_at', 'created_by', 'updated_at', 'updated_by', 'is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        })
    )

@admin.register(Comment)
class CommentAdmin(AuditAdminMixin, admin.ModelAdmin):
    model = Comment

    list_display = ('id', 'short_text', 'article', 'user', 'is_approved')
    list_display_links = ('id', 'article')
    list_filter = ('is_approved',)
    list_per_page = 10
    search_fields = ('article__title', 'user__username', 'text')
    ordering = ('article',)
    actions = ('approve_comments',)

    fieldsets = (
        ('Main Content', {
            'fields': ('article', 'user', 'text', 'is_approved')
        }),
        ('SEO',{
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 'og_title', 'og_description', 'og_image','twitter_title', 'twitter_description', 'twitter_image'),
            'classes': ('collapse',)
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