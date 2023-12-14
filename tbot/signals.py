from django.dispatch import receiver
from django.db.models.signals import post_save
from courses.models import Question, Notes
from tbot.models import TgSpam, TelegramUser
from django.contrib.auth.models import User
from tbot.telegram_bot import bot
# from django_q.tasks import async_task, schedule
# from django_q.models import Schedule
from datetime import timedelta
from django.utils import timezone


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

    # TODO Добавить в сообщение текст заметки
    # TODO c djangoQ на продакшене проблемы

    if created:
        try:
            user = instance.user
            text = 'У вас новая записка на стене \nhttps://django.help/sticky'
            chat_id = TelegramUser.objects.get(user=user).chat_id
            bot.listSender([chat_id], text)
            # async_task(
            #         'tbot.telegram_bot.bot.listSender',
            #         [chat_id],
            #         text,
            #     )

        #     if instance.user == instance.author:
        #         async_task(
        #             'tbot.telegram_bot.bot.listSender',
        #             [chat_id],
        #             text,
        #             hook='tbot.signals.print_result'
        #         )
        #
        #     else:
        #         schedule(
        #             'tbot.telegram_bot.bot.listSender',
        #             [chat_id],
        #             text,
        #             schedule_type=Schedule.ONCE,
        #             next_run=timezone.now() + timedelta(minutes=5),
        #             hook='tbot.signals.print_result'
        #         )
        #
        except:
            pass


def print_result(task):
    print(f'************--hook=main.signals.print_result = {task.result}')