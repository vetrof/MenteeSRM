import telebot
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Profile
from courses.models import Question
from django.contrib.auth.models import User

from tbot.models import TelegramUser

# TODO проверить логику добавления нового юзера по кнопке start

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)


def set_webhook(request):
    webhook_address = settings.TELEGRAM_BOT_WEBHOOK_URL
    bot.remove_webhook()
    bot.set_webhook(webhook_address)
    return HttpResponse(f'<h1>set_webhook---> {settings.TELEGRAM_BOT_WEBHOOK_URL}</h1>')


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
    return HttpResponse('<h1>Bot live!</h1>')

# /START
@bot.message_handler(commands=['start'])
def start(message):

    user_exists = TelegramUser.objects.filter(chat_id=message.chat.id).exists()

    if message.text.endswith('_userid'):
        user_id = message.text.split('/start ')[1]
        user_id = user_id.split('_')[0]

        default_username = "nope"
        default_first_name = "nope"

        try:
            profile = Profile.objects.get(user__id=user_id)
            profile.telegram_chatid = message.chat.id
            profile.save()

            telegram_user = TelegramUser(
                chat_id=message.chat.id,
                username=message.chat.username if message.chat.username else default_username,
                first_name=message.chat.first_name if message.chat.first_name else default_first_name,
                user_id=user_id
            )
            telegram_user.save()

        except Profile.DoesNotExist:
            pass

    if not user_exists:
        telegram_user = TelegramUser(
            chat_id=message.chat.id,
            username=message.chat.username if message.chat.username else default_username,
            first_name=message.chat.first_name if message.chat.first_name else default_first_name,
        )
        telegram_user.save()

    bot.send_message(message.chat.id, f"Привет {message.chat.first_name}! Я ваш телеграм-бот. ")


@bot.message_handler(func=lambda message: True)
def echo_all(message):

    answers = Question.objects.all()
    for answer in answers:
        answer = f' {answer.date} // {answer.client_info} // {answer.text}'
        bot.reply_to(message, answer)


def send_message_for_users(users, text):
    for user in users:
        bot.send_message(user.profile.telegram_chatid, text)








