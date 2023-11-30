from django.urls import path
from .telegram_bot import set_webhook, telegram_webhook
from .views import tbot_personal_link, telegram

# index/tbot/
urlpatterns = [
    path('set_webhook/', set_webhook, name='set_webhook'),
    path('webhook/', telegram_webhook, name='telegram_webhook'),
    path('telegram/', telegram, name='telegram'),
    path('tbot_personal_link/', tbot_personal_link, name='tbot_personal_link'),
]

