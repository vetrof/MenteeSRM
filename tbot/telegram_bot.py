# TODO написать установку хука с помощью терминальной команды

import telebot
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import types

from gcal import g_calendar
from tbot.models import TelegramUser
from tbot.TelebotTelegram import Telegram
from django.urls import reverse

bot = Telegram(settings.TELEGRAM_TOKEN)


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
    chat_id = message.chat.id
    username = message.chat.username if message.chat.username else 'nope',
    first_name = message.chat.first_name if message.chat.first_name else 'nope'
    tg_user_exist = TelegramUser.objects.filter(chat_id=chat_id).exists()

    # get tg_user
    if tg_user_exist:
        tg_user = TelegramUser.objects.get(chat_id=chat_id)
        user_id = tg_user.user_id
    else:
        tg_user = False
        user_id = False

    # get incoming_user_id
    try:
        incoming_user_id = message.text.split()[1]
    except:
        incoming_user_id = None

    if tg_user:
        if not user_id and incoming_user_id:
                tg_user.user_id = incoming_user_id
                tg_user.save()
                user_id = True

    else:
        print('you a here')
        telegram_user = TelegramUser(
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            user_id=incoming_user_id)
        telegram_user.save()

    # messages
    if user_id:
        text = (
            f"Привет {message.chat.first_name} ! Я Django.Help бот. "
            f"Ваш аккаунт на сайте и телеграм успешно связаны.")
    else:
        text = (f"Привет {message.chat.first_name}! Я Django.Help бот."
                f"\nВаш chat_id занесен в базу.\n"
                f"Чтоб связать аккаунт на сайте и ваш телеграм,"
                f" залогинтесь на сайте: \nhttps://django.help/ "
                f"\nи перейдите по этой ссылке: "
                f"\nhttps://django.help/tbot/tbot_personal_link/ "
                f"\nи еще раз активируйте бота")


    # menu
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Info")
    item3 = types.KeyboardButton("Статус")
    item4 = types.KeyboardButton("Чат с ментором")
    item5 = types.KeyboardButton("Расписание")
    # item6 = types.KeyboardButton("Отправить координаты", request_location=True)
    markup.row(item1, item3)
    markup.row(item4, item5)

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markup)


# /Info
@bot.message_handler(func=lambda message: message.text == "Info")
def info(message):

    prefix = settings.HOST
    answer = (f"- Бот сайта: [Django.Help]({prefix})\n"
              f"- Уведомляю о новых записках\n"
              f"- Показываю статус бота\n"
              f"- Дата ближайшего урока \n"
              f"- Помогаю связать чат и ваш аккаунт\n"
              f"- Определить мой IP: [django.help/2ip](https://django.help/2ip/)\n"
              f"- Обновить меню: /start\n"
              )

    bot.send_message(message.chat.id, answer, parse_mode='Markdown')


# /Django.Help
@bot.message_handler(func=lambda message: message.text == "Django.Help")
def djangohelp(message):
    bot.send_message(message.chat.id,
                     "Адрес сайта: [Django.Help](https://django.help/)",
                     parse_mode='Markdown'
                     )


# /Статус
@bot.message_handler(func=lambda message: message.text == "Статус")
def status(message):
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
        link_instructions = (
            f"\nЧтоб связать аккаунт на сайте и ваш телеграм:\n"
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


# /Чат с ментором
@bot.message_handler(func=lambda message: message.text == "Чат с ментором")
def chat(message):
    chat_link = 'https://t.me/VitalyLip'
    bot.send_message(message.chat.id,
                     chat_link,
                     )


# /Расписание
@bot.message_handler(func=lambda message: message.text == "Расписание")
def shedule(message):
    user_id_telegram = message.chat.id
    telegram_user = TelegramUser.objects.get(chat_id=user_id_telegram)
    username = telegram_user.user.username
    superuser = telegram_user.user.is_superuser
    events_list = g_calendar.main()
    answer = ''

    for i in events_list:
        if superuser:
            start_time = i['start']['dateTime']
            timezone = i['start']['timeZone']
            summary = i['summary']
            answer += (
                f'{start_time[:-15]} {start_time[11:-9]} (msk) {summary}\n'
            )
        else:
            if username == i['summary']:
                start_time = i['start']['dateTime']
                timezone = i['start']['timeZone']
                summary = i['summary']
                answer += (
                    f'{start_time[:-15]} {start_time[11:-9]} (msk) \n'
                )

    if answer == '':
        bot.send_message(message.chat.id,
                         'У вас нет занятий в ближайшие 7 дней:')
    else:
        bot.send_message(message.chat.id,
                         f'Ваши занятия в ближайшие 7 дней:\n {answer}',
                         parse_mode='Markdown')


@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    latitude = message.location.latitude
    longitude = message.location.longitude

    # Теперь вы можете отправить координаты и текстовое сообщение на свой бэкенд или выполнить любое нужное действие
    # Пример: Отправка координат и сообщения в вымышленную функцию send_location_and_message_to_backend
    # send_location_and_message_to_backend(chat_id, latitude, longitude, user_message)

    bot.send_message(chat_id, "Координаты и сообщение успешно отправлены!!!!!")
