from sys import path

from django.urls import path, include

from news.views import news

urlpatterns = [
    path('', news, name='news'),

]