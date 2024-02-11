import time
from django.contrib.auth.models import User
from courses.models import Question
from django.http import HttpResponse
from django.conf import settings
import telebot



def new_answer_for_superuser():
    admins = User.objects.filter(is_superuser=True)
    admins_telegram = []
    for admin in admins:
        profile = admin.telegram_id
        telegram_id = profile.current_mentee
        admins_telegram.append(telegram_id)
        

def echo_all(message):
    bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)
    # list answer from index page
    answers = Question.objects.all()
    for answer in answers:
        answer = f' {answer.date} // {answer.client_info} // {answer.text}'
        bot.reply_to(message, answer)


def test():
    bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)
    chat_id = '180958616'
    txt = 'test test'
    for i in range(11):
        bot.send_message(chat_id, f'txt - {i}')

    return HttpResponse('<h1>Bot live!</h1>')



