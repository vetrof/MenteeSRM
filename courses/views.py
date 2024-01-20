from django.contrib import messages
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse

from cabinet.study_class import Study
from courses.forms import NotesForm, QuestionForm
from courses.models import Lesson, Notes

from gcal import g_calendar


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
    course = 'Helpers'
    mentee_id = None
    study = Study(request)
    all_current_mentee = study.mentee_List
    list_for_user = study.list_for_user(mentee_id)
    lessons_and_statuses = study.lessons_list(mentee_id, course, topic_id=None)
    progress = study.progress

    return render(request, 'helpers.html', {
        'course': course,
        'all_current_mentee': all_current_mentee,
        'list_for_user': list_for_user,
        'lessons': lessons_and_statuses,
        'progress': progress,
    })


# @login_required
def lesson_detail(request, id):
    user_g1_status = True
    if request.user.is_anonymous:
        user_g2_status = False
        user_g3_status = False
        user_g0_status = True
    else:
        user_g2_status = request.user.profile.g2
        user_g3_status = request.user.profile.g3
        user_g0_status = True
    lesson = Lesson.objects.get(id=id)
    lesson_grade = lesson.topic.grade.level

    # check permissions
    if lesson_grade == 3 and user_g3_status:
        pass
    elif lesson_grade == 2 and user_g2_status:
        pass
    elif lesson_grade == 1 and user_g1_status:
        pass
    elif lesson_grade == 0 and user_g0_status:
        pass
    else:
        return redirect('no_permissions')

    course = lesson.topic.course.title

    return render(request, 'lesson_detail.html', {'lesson': lesson, "course": course})


@login_required
def calendar(request):
    user = request.user
    if user.profile.current_mentee or user.is_superuser or user.is_staff:
        event_list = {}
        event_list = g_calendar.main()
        return render(request, 'calendar.html', {'event_list': event_list})

    return redirect('no_permissions')


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
def delete_note(request, id, delete):
    if request.user.is_superuser and delete == 'delete':
        note = Notes.objects.get(id=id)
        note.delete()
        # Получаем сохраненный URL предыдущей страницы из сессии
        prev_url = request.session.get('prev_url')

        if prev_url:
            # Перенаправляем пользователя на сохраненную предыдущую страницу
            return redirect(prev_url)
        else:
            # Если URL не сохранен, перенаправляем пользователя на 'sticky_wall' по умолчанию
            return redirect('sticky_wall')

    return render(request, 'sticky_wall.html')


@login_required
def sticky_wall(request, user_id=None):

    if user_id == 0:
        user_id = None
        request.session['look_from_user'] = None
        look_from_user = None
    if user_id:
        request.session['look_from_user'] = user_id
        look_from_user = User.objects.get(id=user_id)
    else:
        look_from_user = None

    try:
        if request.session['look_from_user']:
            user_id = request.session['look_from_user']
            look_from_user = User.objects.get(id=user_id)
            pass
    except:
        request.session['look_from_user'] = request.user.id
        look_from_user = None

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
        'users': users,
        'look_from_user': look_from_user,

    })


def lesson_detail_notion(request):
    data = requests.get(
        'https://different-candle-b8a.notion.site/Google-social-token-3522cedf7b584032a74e73330ff1ea87').text

    return render(request, 'lesson_detail_notion.html', {'data': data})


def no_permissions(request):
    return render(request, 'no_permissions.html')


# landing_page Django
def about_django(request):

    price_1 = '0 ₽'
    price_2 = '500 ₽'
    price_3 = '1.000 ₽'

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    remote_addr = request.META.get('REMOTE_ADDR')
    print('x_forwarded_for', x_forwarded_for)
    print('remote_addr', remote_addr)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    IPINFO_KEY = settings.API_INFO_KEY
    response = requests.get(f'https://ipinfo.io/{ip}?token={IPINFO_KEY}')
    data = response.json()

    try:
        match data['country']:
            case 'KZ':
                price_1 = '0 ₸'
                price_2 = '2.500 ₸'
                price_3 = '5.000 ₸'
            case 'RU':
                price_1 = '0 ₽'
                price_2 = '500 ₽'
                price_3 = '1.000 ₽'
            case _:
                price_1 = '0 $'
                price_2 = '5 $'
                price_3 = '10 $'
    except Exception as err:
        print(err)

    return render(request, 'landing_django_mobi.html', {'price_1': price_1, 'price_2': price_2, 'price_3': price_3, 'data': data})


# landing_page Python
def about_python(request):
    price_1 = '0 ₽'
    price_2 = '500 ₽'
    price_3 = '1.000 ₽'

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(x_forwarded_for, ip)
    IPINFO_KEY = settings.API_INFO_KEY
    response = requests.get(f'https://ipinfo.io/{ip}?token={IPINFO_KEY}')
    data = response.json()

    try:
        match data['country']:
            case 'KZ':
                price_1 = '0 ₸'
                price_2 = '2.500 ₸'
                price_3 = '5.000 ₸'
            case 'RU':
                price_1 = '0 ₽'
                price_2 = '500 ₽'
                price_3 = '1.000 ₽'
            case _:
                price_1 = '0 $'
                price_2 = '5 $'
                price_3 = '10 $'
    except Exception as err:
        print(err)

    return render(request, 'landing_python_mobi.html',
                  {'price_1': price_1, 'price_2': price_2, 'price_3': price_3,
                   'data': data})


def about_fastapi(request):
    price_1 = '0 ₽'
    price_2 = '500 ₽'
    price_3 = '1.000 ₽'

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(x_forwarded_for, ip)
    IPINFO_KEY = settings.API_INFO_KEY
    response = requests.get(f'https://ipinfo.io/{ip}?token={IPINFO_KEY}')
    data = response.json()

    try:
        match data['country']:
            case 'KZ':
                price_1 = '0 ₸'
                price_2 = '2.500 ₸'
                price_3 = '5.000 ₸'
            case 'RU':
                price_1 = '0 ₽'
                price_2 = '500 ₽'
                price_3 = '1.000 ₽'
            case _:
                price_1 = '0 $'
                price_2 = '5 $'
                price_3 = '10 $'
    except Exception as err:
        print(err)

    return render(request, 'landing_fastapi_mobi.html',
                  {'price_1': price_1, 'price_2': price_2, 'price_3': price_3,
                   'data': data})



