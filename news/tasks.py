import pickle
from django.conf import settings
import requests
# from celery import shared_task


# @shared_task()
def get_news_to_dump_file():
    API_KEY = '20039c5603de46b897ab8aeb806cfb10'
    date = '2024-02-09'
    q = 'python'
    link = f'https://newsapi.org/v2/everything?q={q}&from={date}&sortBy=publishedAt&apiKey={API_KEY}'
    data = requests.get(link).json()

    # dump data to file
    with open('news.dump', 'wb') as file:
        pickle.dump(data, file)


# @shared_task()
def test_task():
    print('******* task test *********')
    return 'test ----- task'
