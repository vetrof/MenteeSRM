import time

import telebot


class Telegram(telebot.TeleBot):
    def listSender(self, id_list, text):
        try:
            for chat_id in id_list:
                self.send_message(chat_id, text)
        except:
            pass

    def list_sender_with_optional_image(self, id_list, text, image_link=False):
        if image_link:
                for chat_id in id_list:
                    with open(image_link, 'rb') as image:
                        try:
                            self.send_photo(chat_id, photo=image, caption=text, parse_mode='Markdown')
                            time.sleep(0.3)
                        except Exception as err:
                            print(chat_id, 'image ERROR', err)

        else:
            for chat_id in id_list:
                try:
                    self.send_message(chat_id, text, parse_mode='Markdown')
                    time.sleep(0.5)
                except Exception as err:
                    print('NO image ERROR', err)


