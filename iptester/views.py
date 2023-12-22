from django.conf import settings
import requests

from django.shortcuts import render
from django.http import HttpResponse


def iptester(request):
    x_forward = request.META.get('HTTP_X_FORWARDED_FOR')
    remote_addr = request.META.get('REMOTE_ADDR')

    if x_forward:
        ip = x_forward
    else:
        ip = remote_addr

    response = requests.get(
        f'https://ipinfo.io/{ip}?token={settings.API_INFO_KEY}')
    data = response.json()

    print(data)
    return render(
        request,
        '2ip.html',
        {
            'x_forward': x_forward,
            'remote_addr': remote_addr,
            'data': data
        }
    )
