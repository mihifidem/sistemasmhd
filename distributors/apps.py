from django.apps import AppConfig


class DistributorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'distributors'

    def ready(self):
        from . import signals  # noqa: F401
