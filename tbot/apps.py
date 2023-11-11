from django.apps import AppConfig


class TbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tbot'

    def ready(self):
        import tbot.signals
