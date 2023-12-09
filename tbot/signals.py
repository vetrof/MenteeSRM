from django.dispatch import receiver
from django.db.models.signals import post_save
from courses.models import Question, Notes
from tbot.models import TgSpam, TelegramUser
from django.contrib.auth.models import User
from tbot.telegram_bot import bot


@receiver(post_save, sender=Question)
def question(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(is_superuser=True)
        id_list = []
        for user in users:
            tg_user = TelegramUser.objects.get(user_id=user.id)
            id_list.append(tg_user.chat_id)
        client_info = instance.client_info
        bot.listSender(id_list, client_info)


@receiver(post_save, sender=TgSpam)
def spam_all_tg_user(sender, instance, created, **kwargs):
    if instance.all_tg_user:
        tg_users = TelegramUser.objects.all()
        id_list = []
        for tg_user in tg_users:
            id_list.append(tg_user.chat_id)
        text = f'{instance.title}\n{instance.message}'
        bot.listSender(id_list, text)


@receiver(signal=post_save, sender=Notes)
def new_note(instance, created, **kwargs):

    # TODO сделать отложенную отправку сообщения на 10 минут
    # https: // django - q.readthedocs.io / en / latest / examples.html
    # пример отложенного письма
    # from django_q.tasks import async_task, schedule
    # from django_q.models import Schedule
    # schedule('django.core.mail.send_mail',
    #          'Follow up',
    #          msg,
    #          'from@example.com',
    #          ['recipient@example.com'],
    #          schedule_type=Schedule.ONCE,
    #          next_run=timezone.now() + timedelta(seconds=10))

    # TODO Добавить в сообщение текст заметки

    if created:
        try:
            user = instance.user
            text = 'У вас новая записка на стене \nhttps://django.help/sticky'
            chat_id = TelegramUser.objects.get(user=user).chat_id
            bot.listSender([chat_id], text)
        except:
            pass
