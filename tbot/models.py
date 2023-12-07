from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField


class TelegramUser(models.Model):
    chat_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.chat_id} {self.username} {self.first_name} {self.user}'


class TgSpam(models.Model):
    all_tg_user = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    message = MarkdownxField()

