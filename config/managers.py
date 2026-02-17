from django.db import models
from django.utils import timezone

class AuditSoftDeleteQueryset(models.QuerySet):
    def delete(self, user=None):
        update_data = {
            'is_deleted': True,
            'deleted_at': timezone.now()
        }
        if user:
            update_data['deleted_by'] = user

        return super().update(**update_data)
    
    def restore(self):
        return super().update(
            is_deleted=False,
            deleted_at=None,
            deleted_by=None
        )
    
    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_deleted=False)
    
    def dead(self):
        return self.filter(is_deleted=True)

class AuditSoftDeleteManager(models.Manager):
    def get_queryset(self):
        return AuditSoftDeleteQueryset(self.model, using=self._db).alive()
    
    def dead(self):
        return self.get_queryset().dead()
