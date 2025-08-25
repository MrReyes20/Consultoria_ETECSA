from django.apps import AppConfig


class NotificationSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.notification_system'
    verbose_name = 'Sistema de Notificaciones'

    def ready(self):
        import apps.notification_system.signals  # noqa
