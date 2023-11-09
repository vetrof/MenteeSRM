from django.dispatch import receiver
from django.db.models.signals import post_save

from message.models import SpamForAllUsers
from message.tasks import mail_all_register_user, mail_all_superuser


@receiver(post_save, sender=SpamForAllUsers)
def email_spam_creator(instance, **kwargs):
    if instance.send_now:
        if instance.only_admin:
            mail_all_superuser(instance.id)
        else:
            mail_all_register_user(instance.id)

