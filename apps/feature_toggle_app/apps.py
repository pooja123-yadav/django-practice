from django.apps import AppConfig


class FeatureToggleAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.feature_toggle_app'
