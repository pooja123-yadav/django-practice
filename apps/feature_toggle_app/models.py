from django.db import models


class FeatureToggle(models.Model):
    class TOGGLE_STATE(models.IntegerChoices):
        Enabled = 1, "Enabled"
        Disabled = 0, "Disabled"
    
    class ENVIRONMENT_LEVELS(models.IntegerChoices):
        Global = 1, "Global"
        Development = 2, "Development"
        Production = 3, "Production"

    identifier  = models.CharField(max_length=100, unique=True, db_index= True)
    description = models.CharField(max_length=200, null= True, blank=True)
    state       = models.IntegerField(choices=TOGGLE_STATE.choices, default=TOGGLE_STATE.Enabled, db_index=True)
    environment = models.IntegerField(choices=ENVIRONMENT_LEVELS.choices, default= ENVIRONMENT_LEVELS.Global, db_index=True)
    notes       = models.TextField(null= True, blank=True)
    created_by  = models.PositiveIntegerField(null= True, blank= True, db_index=True, verbose_name='Created By')
    updated_by  = models.PositiveIntegerField(null= True, blank= True, db_index=True, verbose_name='Updated By')
    is_deleted  = models.BooleanField(default=False, verbose_name='Deleted', db_index=True)
    created_at  = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Date')
    updated_at  = models.DateTimeField(auto_now=True, verbose_name='Updated Date')

    def __str__(self):
            return str(self.identifier)

    class Meta:
        ordering = ['-id']
        db_table = 'feature_toggle'
        verbose_name = 'Feature Toggle'
        verbose_name_plural = 'Features Toggle'