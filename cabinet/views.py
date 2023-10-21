from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from courses.models import Lesson, LessonStatus


def cabinet(request, user_id=None):
    current_user = request.user.id
    users = {}
    username = request.user
    if request.user.is_authenticated:

        if request.user.is_superuser and user_id != None:
            user = User.objects.get(id=user_id)
            current_user = user_id
            username = user
            lessons = Lesson.objects.all().order_by('grade', 'topic__num_topic', 'num_lesson')
            lesson_statuses = LessonStatus.objects.filter(user=user, lesson__in=lessons)
        else:
            lessons = Lesson.objects.all().order_by('grade', 'topic__num_topic', 'num_lesson')
            lesson_statuses = LessonStatus.objects.filter(user=request.user, lesson__in=lessons)


        g1_progress, g2_progress, g3_progress = 0, 0, 0

        # calculate progress
        lessons_g1 = lesson_statuses.filter(lesson__grade=1)
        lessons_g1_done = lessons_g1.filter(status='done')
        lessons_g2 = lesson_statuses.filter(lesson__grade=2)
        lessons_g2_done = lessons_g2.filter(status='done')
        lessons_g3 = lesson_statuses.filter(lesson__grade=3)
        lessons_g3_done = lessons_g3.filter(status='done')

        try:
            g1_progress = round(len(lessons_g1_done) / (len(lessons_g1) / 100))
            g2_progress = round(len(lessons_g2_done) / (len(lessons_g2) / 100))
            g3_progress = round(len(lessons_g3_done) / (len(lessons_g3) / 100))
        except:
            ...

        progress = {'g1_progress': g1_progress, 'g2_progress': g2_progress, 'g3_progress': g3_progress}

        lessons_dict = []
        for lesson in lessons:
            add = {
                'id': lesson.id,
                'grade': lesson.grade,
                'topic': lesson.topic.title,
                'title': lesson.title,
                'get_absolute_url': lesson.get_absolute_url,
            }
            for status in lesson_statuses:
                if status.lesson.id == lesson.id:
                    add['status'] = status.status
            lessons_dict.append(add)
    else:
        lessons = Lesson.objects.all().order_by('grade', 'topic__num_topic', 'num_lesson')
        lessons_dict = []
        for lesson in lessons:
            add = {
                'id': lesson.id,
                'grade': lesson.grade,
                'topic': lesson.topic.title,
                'title': lesson.title,
                'get_absolute_url': lesson.get_absolute_url,
            }

            lessons_dict.append(add)
        return render(request, 'cabinet.html', {'lessons': lessons_dict})

    # view lesson as user
    if request.user.is_superuser:
        users = User.objects.all()


    return render(request, 'cabinet.html', {'lessons': lessons_dict, 'progress': progress, 'users': users, 'current_user': current_user, 'username': username})


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
