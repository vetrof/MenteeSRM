from django.urls import path
from cabinet.views import change_lesson_status, course_cabinet

# /cabinet/
urlpatterns = [
    path('<str:course>/<int:topic>/', course_cabinet, name='course_cabinet'),
    path('<str:course>/', course_cabinet, name='course_cabinet'),
    path('mentee_id/<int:mentee_id>/course/<str:course>', course_cabinet, name='course_cabinet_mentee_id'),
    path('mentee_id/<int:mentee_id>/course/<str:course>/<int:topic>/', course_cabinet, name='course_cabinet_mentee_id'),
    path('change_lesson_status/', change_lesson_status, name='change_lesson_status'),
    path('change_lesson_status/<int:user_id>', change_lesson_status, name='change_lesson_status'),

]