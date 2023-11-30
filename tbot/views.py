from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings


def telegram(request):
    return render(request, 'telegram.html')


def tbot_personal_link(request):
    if request.user.is_authenticated:
        tbot_link = f"{settings.TELEGRAM_LINK}?start={request.user.id}_userid"
        return redirect(tbot_link)
    return redirect(settings.TELEGRAM_LINK)