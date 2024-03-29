from django.urls import path, include
from courses.views import (index_page, contacts_page, helpers_page,
                           lesson_detail, calendar, sticky_wall,
                           edit_note, delete_note, lesson_detail_notion,
                           no_permissions, about_django, about_python, about_fastapi)

# index/...
urlpatterns = [
    path('contacts/', contacts_page, name='contacts'),
    path('helpers/', helpers_page, name='helpers'),
    path('lesson/<int:id>/', lesson_detail, name='lesson_detail'),
    path('calendar/', calendar, name='calendar'),
    path('sticky/', sticky_wall, name='sticky_wall'),
    path('sticky/user/<int:user_id>', sticky_wall, name='sticky_wall_user_id'),
    path('sticky/<int:id>/', edit_note, name='edit_note'),
    path('sticky/<int:id>/<str:delete>/', delete_note, name='delete_note'),
    path('markdownx/', include('markdownx.urls')),

    path('lesson_notion/', lesson_detail_notion, name='lesson_detail_notion'),
    path('no_permissions/', no_permissions, name='no_permissions'),

    path('', index_page, name='index'),

    # landing pages
    path('about_django/', about_django, name='about_django'),
    path('about_python/', about_python, name='about_python'),
    path('about_fastapi/', about_fastapi, name='about_fastapi'),

]