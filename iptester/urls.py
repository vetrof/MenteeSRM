from django.urls import path, include

from iptester.views import iptester

#  index/2ip/...
urlpatterns = [
    path('', iptester)
]