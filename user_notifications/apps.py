from django.apps import AppConfig


class UserNotificationsConfig(AppConfig):
    name = 'user_notifications'
    verbose_name = 'Notifications'

    def ready(self):
        super().ready()
        # this is for backwards compability
        import user_notifications.signals
        user_notifications.notify = user_notifications.signals.notify
