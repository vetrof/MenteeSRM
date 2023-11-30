from django.db import models
from django.contrib.auth.models import User


class TelegramUser(models.Model):
    chat_id = models.IntegerField()
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

