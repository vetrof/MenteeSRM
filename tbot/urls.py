from django.urls import path
from .telegram_bot import set_webhook, telegram_webhook

# index/tbot/
urlpatterns = [
    path('set_webhook/', set_webhook, name='set_webhook'),
    path('webhook/', telegram_webhook, name='telegram_webhook'),
]

