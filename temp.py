основные команды терминала

python3 -m venv myworld                 # создание окружения
source myworld/bin/activate             # активация окружения
-m pip install Django                   # установка джанго
python3 -m django --version             # версия
django-admin startproject myroject .    # создание проекта
python3 manage.py startapp myapp        # создание приложения
python3 manage.py runserver             # отладочный сервер
python3 manage.py makemigrations        # создание миграций
python3 manage.py migrate               # применение миграций
python3 manage.py createsuperuser       # создание суперпользователя
pip freeze > requirements.txt           # создание файла зависимостей
pip install -r requirements.txt         # установка зависимостей

