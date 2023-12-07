import telebot


class Telegram(telebot.TeleBot):

    def listSender(self, id_list, text):
        for chat_id in id_list:
            self.send_message(chat_id, text)
