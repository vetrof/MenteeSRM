from django.dispatch import receiver
from django.db.models.signals import post_save
from courses.models import Question
from tbot.models import TgSpam, TelegramUser
from tbot.telegram_bot import TelegramSender
from django.contrib.auth.models import User


@receiver(post_save, sender=Question)
def question_to_telegram(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(is_superuser=True)
        client_info = instance.client_info
        TelegramSender.send_message_for_users(users, client_info)


@receiver(post_save, sender=TgSpam)
def spam_all_tg_user(sender, instance, created, **kwargs):
    if instance.all_tg_user:
        users = TelegramUser.objects.all()
        title = instance.title
        text = instance.message
        TelegramSender.spam_all_user(users, title, text)
