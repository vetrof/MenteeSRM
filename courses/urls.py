from django.urls import path
from cabinet.views import cabinet, change_lesson_status
from courses.views import index_page, contacts_page, helpers_page, lesson_detail

# index/...
urlpatterns = [
    path('contacts/', contacts_page, name='contacts'),
    path('helpers/', helpers_page, name='helpers'),
    path('lesson/<int:id>/', lesson_detail, name='lesson_detail'),
    path('', index_page, name='index'),

]