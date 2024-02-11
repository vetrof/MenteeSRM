import pickle

from django.http import HttpResponse
from django.shortcuts import render

from news.tasks import get_news_to_dump_file


def news(request):
    all_news = []

    with open('news.dump', 'rb') as file:
        all_news = pickle.load(file)

    return render(request, 'news.html', {'all_news': all_news})


def news_update(request):
    get_news_to_dump_file()
    return HttpResponse('Updated')
