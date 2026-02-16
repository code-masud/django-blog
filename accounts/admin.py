from django.contrib import admin
from .models import Company, Profile, Contact
from django.utils.html import format_html

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    
    list_display = ['id', 'name', 'preview_logo', 'phone', 'email']
    list_display_links = ['id', 'name']
    list_filter = ['name']
    list_per_page = 10
    search_fields = ['name', 'phone', 'address']
    ordering = ['name']

    def preview_logo(self, obj):
        if obj.logo:
            return format_html(
                '<img src={} style="width:20px; height:20px;">',
                obj.logo.url
            )
        return '--'
    preview_logo.short_description = 'logo'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    
    list_display = ['id', 'user', 'preview_avatar', 'phone', 'email', 'name']
    list_display_links = ['id', 'user']
    list_filter = ['user']
    list_per_page = 10
    search_fields = ['user', 'phone', 'name']
    ordering = ['user']

    def preview_avatar(self, obj):
        if obj.avatar:
            return format_html(
                '<img src={} style="width:20px; height:20px;">',
                obj.avatar.url
            )
        return '--'
    preview_avatar.short_description = 'avatar'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    model = Contact
    
    list_display = ['id', 'name', 'phone', 'email', 'message']
    list_display_links = ['id', 'name']
    list_filter = ['name']
    list_per_page = 10
    search_fields = ['name', 'phone', 'message']
    ordering = ['name']