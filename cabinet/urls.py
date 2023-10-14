from django.urls import path
from cabinet.views import cabinet, change_lesson_status

urlpatterns = [
    path('', cabinet, name='cabinet'),
    path('change_lesson_status/', change_lesson_status, name='change_lesson_status'),

]