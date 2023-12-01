from django.contrib import admin

from tbot.models import TelegramUser, TgSpam

admin.site.register(TelegramUser)
admin.site.register(TgSpam)
