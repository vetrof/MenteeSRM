from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from tbot.models import TelegramUser
from tbot.telegram_bot import send_massage_to_user
from .models import Notes

@receiver(signal=post_save, sender=Notes)
def new_note_to_telegram(instance, created, **kwargs):
    if created:
        try:
            user = instance.user
            text = 'У вас новая записка на стене \nhttps://django.help/sticky'
            chat_id = TelegramUser.objects.get(user=user).chat_id
            send_massage_to_user(chat_id,
                                 f'Привет {user.username}! ',
                                 text)
        except:
            pass
