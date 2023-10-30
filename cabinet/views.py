from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from cabinet.study_class import Study

from courses.models import Lesson, LessonStatus, Course


def course_cabinet(request, mentee_id=None, course=None):

    study = Study(request)
    all_current_mentee = study.mentee_List
    list_for_user = study.list_for_user(mentee_id)
    lessons_and_statuses = study.lessons_list(mentee_id, course)
    progress = study.progress

    return render(request, 'cabinet.html', {
        'course': course,
        'all_current_mentee': all_current_mentee,
        'list_for_user': list_for_user,
        'lessons': lessons_and_statuses,
        'progress': progress,
    })


@login_required
def change_lesson_status(request, user_id=None):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        status = request.POST.get('status')
        lesson_status, created = LessonStatus.objects.get_or_create(user=user, lesson_id=lesson_id)
        lesson_status.status = status
        lesson_status.save()
        return JsonResponse({'message': 'Статус успешно изменен'})
    return JsonResponse({'message': 'Ничего не изменилось'})
