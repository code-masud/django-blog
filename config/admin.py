from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages


class AuditAdminMixin:
    
    @admin.action(description='Hard delete selected items')
    def hard_delete(self, request, queryset):
        count = 0
        for obj in queryset:
            count += 1
            obj.hard_delete()
        
        self.message_user(request, f'{count} items hard deleted successfully.')

    @admin.action(description="Restore selected items")
    def restore_selected(self, request, queryset):
        restored_count = 0
        for obj in queryset.filter(is_deleted=True):
            obj.is_deleted = False
            obj.deleted_at = None
            obj.deleted_by = None
            obj.save()

            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(obj).pk,
                object_id=obj.pk,
                object_repr=str(obj),
                action_flag=CHANGE,
                change_message="Restored via admin"
            )
            restored_count += 1

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
        actions["hard_delete"] = (
            self.__class__.hard_delete,
            "hard_delete",
            "Hard delete selected items",
        )
        return actions
    
    def get_list_display(self, request):
        return super().get_list_display(request) + ('restore_button', 'is_deleted',)

    def get_list_filter(self, request):
        return super().get_list_filter(request) + ('is_deleted', 'created_at', 'updated_at', 'deleted_at')

    def get_readonly_fields(self, request, obj):
        return super().get_readonly_fields(request, obj) + ('created_at', 'updated_at')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/restore/', self.admin_site.admin_view(self.restore_view), name=f'{self.__class__.__name__}_object-restore'),
        ]
        return custom_urls + urls

    def restore_view(self, request, pk):
        obj = self.get_object(request, pk)
        obj.restore()
        self.message_user(request, f"{obj} restored successfully.")
        return redirect(request.META.get("HTTP_REFERER"))
    
    def restore_button(self, obj):
        if obj.is_deleted:
            return format_html(
                '<a class="restore-btn" href="{}">Restore</a>',
                reverse(f"admin:{self.__class__.__name__}_object-restore", args=[obj.pk])
            )
        return "-"
    restore_button.short_description = "Restore"
    restore_button.allow_tags = True

    def get_queryset(self, request):
        return self.model.all_objects.all()

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.delete(user=request.user)
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=DELETION,
            change_message="Soft deleted via admin"
        )

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete(user=request.user)
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(obj).pk,
                object_id=obj.pk,
                object_repr=str(obj),
                action_flag=DELETION,
                change_message="Soft deleted via admin"
            )