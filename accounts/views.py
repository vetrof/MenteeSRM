from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

from accounts.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from accounts.models import Profile

from django.db.models import F, ExpressionWrapper, FloatField, Case, When, Value, CharField

import time

import threading

from courses.models import Lesson, LessonStatus
from django.http import JsonResponse


def index_views(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    # lessons = Lesson.objects.all().order_by('grade', 'topic__num_topic', 'num_lesson')
    # lesson_statuses = LessonStatus.objects.filter(user=request.user, lesson__in=lessons)
    # lessons_dict = []
    # for lesson in lessons:
    #     add = {}
    #     add['id'] = lesson.id
    #     add['grade'] = lesson.grade
    #     add['topic'] = lesson.topic.title
    #     add['title'] = lesson.title
    #     for status in lesson_statuses:
    #         if status.lesson.id == lesson.id:
    #             add['status'] = status.status
    #     lessons_dict.append(add)
    return render(request, 'account/dashboard.html', )
    # return render(request, 'account/dashboard.html', {'lessons': lessons, 'lesson_statuses': lesson_statuses})


@login_required
def change_lesson_status(request):
    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        status = request.POST.get('status')
        lesson_status, created = LessonStatus.objects.get_or_create(user=request.user, lesson_id=lesson_id)
        lesson_status.status = status
        lesson_status.save()
        return JsonResponse({'message': 'Статус успешно изменен'})
    return JsonResponse({'message': 'Ничего не изменилось'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

