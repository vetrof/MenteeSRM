from sys import path

from django.urls import path, include

from news.views import news, news_update

urlpatterns = [
    path('', news, name='news'),
    path('update/', news_update, name='news_update'),

]