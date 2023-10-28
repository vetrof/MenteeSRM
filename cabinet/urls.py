from django.urls import path
from cabinet.views import cabinet, change_lesson_status
# /cabinet/
urlpatterns = [
    path('<str:course_name>/', cabinet, name='cabinet'),
    path('user/<int:user_id>', cabinet, name='cabinet_user_id'),
    path('change_lesson_status/', change_lesson_status, name='change_lesson_status'),
    path('change_lesson_status/<int:user_id>', change_lesson_status, name='change_lesson_status'),

]