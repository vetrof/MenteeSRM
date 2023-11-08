
from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse

from courses.forms import NotesForm, QuestionForm
from courses.models import Lesson, Notes


def index_page(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение отправлено')  # Добавляем сообщение
            return render(request, 'message_succes.html')

    form = QuestionForm()
    return render(request, 'index.html')


def contacts_page(request):
    return render(request, 'contacts.html')


def helpers_page(request):
    return render(request, 'helpers.html')


@login_required
def lesson_detail(request, id):
    user_g1_status = True
    user_g2_status = request.user.profile.g2
    user_g3_status = request.user.profile.g3
    lesson = Lesson.objects.get(id=id)
    lesson_grade = lesson.topic.grade.level

    # check permissions
    if lesson_grade == 3 and user_g3_status:
        pass
    elif lesson_grade == 2 and user_g2_status:
        pass
    elif lesson_grade == 1 and user_g1_status:
        pass
    else:
        return redirect('no_permissions')

    return render(request, 'lesson_detail.html', {'lesson': lesson})


@login_required
def calendar(request):
    return render(request, 'calendar.html')


@login_required
def edit_note(request, id):
    note = Notes.objects.get(id=id)
    if request.user != note.user and not request.user.is_staff:
        # Защита от редактирования чужих записок
        return redirect('sticky_wall')

    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()

            # Получаем сохраненный URL предыдущей страницы из сессии
            prev_url = request.session.get('prev_url')

            if prev_url:
                # Перенаправляем пользователя на сохраненную предыдущую страницу
                return redirect(prev_url)
            else:
                # Если URL не сохранен, перенаправляем пользователя на 'sticky_wall' по умолчанию
                return redirect('sticky_wall')
    else:
        form = NotesForm(instance=note)

        # Сохраняем текущий URL в сессии как предыдущий URL
        request.session['prev_url'] = request.META.get('HTTP_REFERER')

    return render(request, 'sticky_wall.html', {'form': form})


@login_required
def sticky_wall(request, user_id=None):
    if user_id and request.user.is_superuser:
        current_user = User.objects.get(id=user_id)
    else:
        current_user = request.user

    users = User.objects.filter(profile__current_mentee=True)
    notes = Notes.objects.filter(user=current_user).order_by('-id').exclude(on_top=True)
    top_notes = Notes.objects.filter(user=current_user, on_top=True).order_by('-id')

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

    return render(request, 'sticky_wall.html', {
        'top_notes': top_notes,
        'notes': notes,
        'form': form,
        'current_user': current_user,
        'users': users
    })


def lesson_detail_notion(request):
    data = requests.get(
        'https://different-candle-b8a.notion.site/Google-social-token-3522cedf7b584032a74e73330ff1ea87').text

    return render(request, 'lesson_detail_notion.html', {'data': data})


def no_permissions(request):
    return render(request, 'no_permissions.html')