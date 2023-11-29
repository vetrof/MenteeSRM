from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from cabinet.study_class import Study
import time

from courses.models import Lesson, LessonStatus, Course


def course_cabinet(request, mentee_id=None, course=None, topic=None):
    start_time_without_index = time.time()

    if mentee_id == 0:
        mentee_id = None
        look_from_user = None
        request.session['look_from_user'] = None

    if mentee_id:
        request.session['look_from_user'] = mentee_id
        look_from_user = User.objects.get(id=mentee_id)
    else:
        look_from_user = None

    try:
        if request.session['look_from_user']:
            mentee_id = request.session['look_from_user']
            look_from_user = User.objects.get(id=mentee_id)
            pass
    except:
        request.session['look_from_user'] = request.user.id

    topic_id = topic
    study = Study(request)
    all_current_mentee = study.mentee_List
    list_for_user = study.list_for_user(mentee_id)
    lessons_and_statuses = study.lessons_list(mentee_id, course, topic_id)
    progress = study.progress

    # time process
    end_time_without_index = time.time()
    time_taken_without_index = end_time_without_index - start_time_without_index
    print(f'Time taken without index: {time_taken_without_index} seconds')

    return render(request, 'cabinet.html', {
        'course': course,
        'topic': topic,
        'all_current_mentee': all_current_mentee,
        'list_for_user': list_for_user,
        'lessons': lessons_and_statuses,
        'progress': progress,
        'look_from_user': look_from_user,
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
