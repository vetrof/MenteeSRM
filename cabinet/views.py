from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from courses.models import Lesson, LessonStatus


@login_required
def cabinet(request):
    lessons = Lesson.objects.all().order_by('grade', 'topic__num_topic', 'num_lesson')
    lesson_statuses = LessonStatus.objects.filter(user=request.user, lesson__in=lessons)

    # calculate progress
    lessons_g1 = lesson_statuses.filter(lesson__grade=1)
    lessons_g1_done = lessons_g1.filter(status='done')
    lessons_g2 = lesson_statuses.filter(lesson__grade=2)
    lessons_g2_done = lessons_g2.filter(status='done')
    lessons_g3 = lesson_statuses.filter(lesson__grade=3)
    lessons_g3_done = lessons_g3.filter(status='done')

    g1_progress, g2_progress, g3_progress = 0, 0, 0

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

    return render(request, 'cabinet.html', {'lessons': lessons_dict, 'progress': progress})


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
