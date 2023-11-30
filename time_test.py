import os

import django

# Указать путь к файлу settings.py в переменной окружения
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "VetrofPerScoolProject.settings")
django.setup()

import time
from tbot.models import TelegramUser

# Измерение времени выполнения запроса без индекса
start_time_without_index = time.time()

t_user = TelegramUser.objects.create(
    chat_id=7,
    username='vetrof',
    first_name='votaly',
    user_id=18,
)

end_time_without_index = time.time()
time_taken_without_index = end_time_without_index - start_time_without_index
print(f'Time taken without index: {time_taken_without_index} seconds')
