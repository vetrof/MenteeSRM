from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from courses.models import Lesson


def index_page(request):
    return render(request, 'index.html')


def contacts_page(request):
    return render(request, 'contacts.html')


def helpers_page(request):
    return render(request, 'helpers.html')


@login_required
def lesson_detail(request, id):
    lesson = Lesson.objects.get(id=id)
    return render(request, 'lesson_detail.html', {'lesson': lesson})


@login_required
def calendar(request):
    return render(request, 'calendar.html')
