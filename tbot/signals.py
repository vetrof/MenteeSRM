from django.dispatch import receiver
from django.db.models.signals import post_save
from courses.models import Question
from tbot.telegram_bot import send_message_for_users
from django.contrib.auth.models import User


@receiver(post_save, sender=Question)
def question_to_telegram(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(is_superuser=True)
        date = instance.date
        client_info = instance.client_info
        text = instance.text
        send_message_for_users(users, client_info)

