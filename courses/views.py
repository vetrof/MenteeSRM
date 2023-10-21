import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from courses.forms import NotesForm, QuestionForm
from courses.models import Lesson, Notes


def index_page(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()


    form = QuestionForm()
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


@login_required
def edit_note(request, id):
    note = Notes.objects.get(id=id)
    if request.user != note.user:
        # Защита от редактирования чужих записок
        return redirect('sticky_wall')

    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('sticky_wall')
    else:
        form = NotesForm(instance=note)

    return render(request, 'sticky_wall.html', {'form': form})


@login_required
def sticky_wall(request, user_id=None):
    if user_id and request.user.is_superuser:
        current_user = User.objects.get(id=user_id)
    else:
        current_user = request.user

    users = User.objects.all()
    notes = Notes.objects.filter(user=current_user).order_by('-id')

    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = current_user
            note.author = request.user
            note.save()
            return redirect('sticky_wall')
    else:
        form = NotesForm()

    return render(request, 'sticky_wall.html', {'notes': notes, 'form': form, 'current_user': current_user, 'users': users})


def lesson_detail_notion(request):
    data = requests.get(
        'https://different-candle-b8a.notion.site/Google-social-token-3522cedf7b584032a74e73330ff1ea87').text

    return render(request, 'lesson_detail_notion.html', {'data': data})