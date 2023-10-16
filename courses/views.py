from django.shortcuts import render

from courses.models import Lesson


def index_page(request):
    return render(request, 'index.html')


def contacts_page(request):
    return render(request, 'contacts.html')


def helpers_page(request):
    return render(request, 'helpers.html')


def lesson_detail(request, id):
    lesson = Lesson.objects.get(id=id)
    return render(request, 'lesson_detail.html', {'lesson': lesson})
