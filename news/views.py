import pickle

from django.shortcuts import render


def news(request):
    all_news = []

    with open('news.dump', 'rb') as file:
        all_news = pickle.load(file)

    return render(request, 'news.html', {'all_news': all_news})
