from django.urls import path, include
from cabinet.views import cabinet, change_lesson_status
from courses.views import index_page, contacts_page, helpers_page, lesson_detail, calendar, sticky_wall, edit_note, lesson_detail_notion

# index/...
urlpatterns = [
    path('contacts/', contacts_page, name='contacts'),
    path('helpers/', helpers_page, name='helpers'),
    path('lesson/<int:id>/', lesson_detail, name='lesson_detail'),
    path('calendar/', calendar, name='calendar'),
    path('sticky/', sticky_wall, name='sticky_wall'),
    path('sticky/user/<int:user_id>', sticky_wall, name='sticky_wall_user_id'),
    path('sticky/<int:id>', edit_note, name='edit_note'),
    path('markdownx/', include('markdownx.urls')),

    path('lesson_notion/', lesson_detail_notion, name='lesson_detail_notion'),

    path('', index_page, name='index'),

]