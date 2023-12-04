import telebot
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import types

from accounts.models import Profile
from cabinet.study_class import Study
from courses.models import Question
from django.contrib.auth.models import User

from tbot.models import TelegramUser

# TODO проверить логику добавления нового юзера по кнопке start

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)


def set_webhook(request):
    webhook_address = settings.TELEGRAM_BOT_WEBHOOK_URL
    bot.remove_webhook()
    bot.set_webhook(webhook_address)
    return HttpResponse(
        f'<h1>set_webhook---> {settings.TELEGRAM_BOT_WEBHOOK_URL}</h1>')


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
    return HttpResponse('<h1>Bot live!</h1>')


# /START
@bot.message_handler(commands=['start'])
def start(message):
    text = ""
    chat_id = message.chat.id
    username = message.chat.username if message.chat.username else 'nope',
    first_name = message.chat.first_name if message.chat.first_name else 'nope'
    tg_user_exist = TelegramUser.objects.filter(chat_id=chat_id).exists()

    print(chat_id, username, first_name, tg_user_exist)

    # user зареган на сайте
    if message.text.endswith('_userid'):

        # его chat id  есть в базе
        if tg_user_exist:
            # у него есть user id
            user_id_exists = TelegramUser.objects.get(chat_id=chat_id)
            if user_id_exists.user_id:
                pass

            # у него нет user id
            else:
                # получаем id из message
                all_text = message.text.split('/start ')[1]
                user_id = all_text.split('_')[0]
                # добавляем user id
                tg_user = TelegramUser.objects.get(chat_id=chat_id)
                tg_user.user_id = user_id
                tg_user.save()

        else:
            # получаем id из message
            all_text = message.text.split('/start ')[1]
            user_id = all_text.split('_')[0]

            # добавляем нового tg юзера
            telegram_user = TelegramUser(
                chat_id=chat_id,
                username=username,
                first_name=first_name,
                user_id=user_id
            )
            telegram_user.save()
        # text = f"Привет {message.chat.first_name}! Я Django.Help бот."

    # юзер не зареган на сайте
    else:
        try:

            # добавляем нового tg юзера
            new_tg_user = TelegramUser(chat_id=chat_id,
                                       username=username,
                                       first_name=first_name)
            new_tg_user.save()

        except:
            ...

    try:
        user_id = TelegramUser.objects.get(chat_id=chat_id).user_id
        text = (f"Привет {message.chat.first_name}! Я Django.Help бот. "
                f"Ваш аккаунт на сайте и телеграм успешно связаны.")
    except:
        text = (f"Привет {message.chat.first_name}! Я Django.Help бот."
                f"\nВаш chat_id занесен в базу.\n"
                f"Чтоб связать аккаунт на сайте и ваш телеграм,"
                f" залогинтесь на сайте: \nhttps://django.help/ "
                f"\nи перейдите по этой ссылке: "
                f"\nhttps://django.help/tbot/tbot_personal_link/ "
                f"\nи еще раз активируйте бота")

    # menu
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Что я умею")
    item2 = types.KeyboardButton("Django.Help")
    item3 = types.KeyboardButton("Статус")
    markup.row(item1, item2, item3)

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markup
                     )


# /Что я умею
@bot.message_handler(func=lambda message: message.text == "Что я умею")
def start(message):
    bot.send_message(message.chat.id,
                     "- Уведомляю о новых записках\n"
                     "- Показываю статус бота\n"
                    "- Дата ближайшего урока (скоро)\n"
                    "- Помогаю связать чат и ваш аккаунт\n", parse_mode='Markdown'
                     )


# /Django.Help
@bot.message_handler(func=lambda message: message.text == "Django.Help")
def start(message):
    bot.send_message(message.chat.id,
                     "Адрес сайта: [Django.Help](https://django.help/)",
                     parse_mode='Markdown'
                     )


# /Статус
@bot.message_handler(func=lambda message: message.text == "Статус")
def start(message):

    user_id_telegram = message.chat.id
    username_telegram = message.chat.username
    first_name_telegram = message.chat.first_name
    try:
        telegram_user = TelegramUser.objects.get(chat_id=user_id_telegram)
        user_id = telegram_user.user_id
        username_site = telegram_user.user.username
    except Exception as err:
        user_id = False
        username_site = False
        print(err)

    link_status = 'True' if user_id else 'False'

    if not user_id:
        link_instructions = (f"\nЧтоб связать аккаунт на сайте и ваш телеграм:\n"
                            f"\nзалогинтесь на сайте: "
                            f"\nhttps://django.help\n"
                            f"\nперейдите в настройки аккаунта: "
                            f"\nhttps://django.help/account\n"
                            f"\nперейдите по ссылке 'Подключить телеграм бот': "
                            f"\nhttps://django.help/tbot/tbot_personal_link\n"
                            f"\nи еще раз активируйте бота")
    else:
        link_instructions = ''

    answer = (f"Статус синхронизации = {link_status}\n\n"
              f"Телеграмм:\n"
              f"id = {user_id_telegram}\n"
              f"username = {username_telegram}\n"
              f"first_name = {first_name_telegram}\n"
              f"\nСайт:\n"
              f"user_id = {user_id}\n"
              f"username = {username_site}\n"
              f"{link_instructions}\n"
              )


    bot.send_message(message.chat.id,
                     answer,
                     )


def send_message_for_users(users, text):
    for user in users:
        bot.send_message(user.profile.telegram_chatid, text)


def spam_all_user(users, title, text):
    message = f"*{title}*\n{text}"
    for user in users:
        bot.send_message(user.chat_id, message, parse_mode='Markdown')


def send_massage_to_user(chat_id, title, text):
    message = f"\n*{title}*\n{text}"
    bot.send_message(chat_id, message, parse_mode='Markdown')
