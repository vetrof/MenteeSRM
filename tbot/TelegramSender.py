import telebot
from django.conf import settings


class TelegramSender:
    def __init__(self):
        self.bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

    def send_message(self, id_list, message):
        for user in id_list:
            self.bot.send_message(user.profile.telegram_chatid, message)