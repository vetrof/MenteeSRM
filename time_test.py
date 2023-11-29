import os
import django

# Указать путь к файлу settings.py в переменной окружения
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VetrofPerScoolProject.settings")
django.setup()

from courses.models import Lesson
from django.contrib.auth.models import User


import time

# Измерение времени выполнения запроса без индекса
start_time_without_index = time.time()


x = Lesson.objects.filter(title__icontains='SSL').count()




end_time_without_index = time.time()
time_taken_without_index = end_time_without_index - start_time_without_index
print(f'Time taken without index: {time_taken_without_index} seconds')

