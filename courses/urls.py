from django.urls import path
from cabinet.views import cabinet, change_lesson_status
from courses.views import index_page, contacts_page, helpers_page

urlpatterns = [
    path('', index_page, name='index'),
    path('contacts/', contacts_page, name='contacts'),
    path('helpers/', helpers_page, name='helpers'),

]