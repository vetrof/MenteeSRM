import os

import django

# Указать путь к файлу settings.py в переменной окружения
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "VetrofPerScoolProject.settings")
django.setup()

import time
from tbot.models import TelegramUser
from django.contrib.auth.models import User

# Измерение времени выполнения запроса без индекса
start_time_without_index = time.time()

try:
    telegram_user = TelegramUser.objects.get(user_id=18)
    chat_id = telegram_user.chat_id
except TelegramUser.DoesNotExist:
    chat_id = None
except Exception as e:
    print(f"Произошла ошибка: {e}")

print(chat_id)


end_time_without_index = time.time()
time_taken_without_index = end_time_without_index - start_time_without_index
print(f'Time taken without index: {time_taken_without_index} seconds')
