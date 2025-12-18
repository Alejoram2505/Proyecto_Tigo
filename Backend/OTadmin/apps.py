from django.apps import AppConfig

class OTadminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "OTadmin"

    def ready(self):
        import OTadmin.signals  # noqa
