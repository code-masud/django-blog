from django.contrib import admin
from django.utils.html import format_html

class AuditAdminMixin:

    @admin.action(description="Restore selected items")
    def restore_selected(self, request, queryset):
        deleted_qs = queryset.filter(is_deleted=True)

        restored_count = deleted_qs.update(
            is_deleted=False,
            deleted_at=None,
            deleted_by=None,
        )

        self.message_user(
            request,
            f"{restored_count} item(s) restored successfully.",
        )
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        actions["restore_selected"] = (
            self.__class__.restore_selected,
            "restore_selected",
            "Restore selected items",
        )
        return actions
    
    def get_list_display(self, request):
        return super().get_list_display(request) + ('is_deleted', 'deleted_status',)

    def get_list_filter(self, request):
        return super().get_list_filter(request) + ('is_deleted', 'created_at', 'updated_at', 'deleted_at')

    def get_readonly_fields(self, request, obj):
        return super().get_readonly_fields(request, obj) + ('created_at', 'updated_at')
    
    @admin.display(description="Delete Status")
    def deleted_status(self, obj):
        if obj.is_deleted:
            return format_html('<span style="color:red;font-weight:bold;">Deleted</span>')
        return "Active"
    
    def get_queryset(self, request):
        return self.model.all_objects.all()
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.delete(user=request.user)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete(user=request.user)