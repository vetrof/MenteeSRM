from django.contrib.auth.models import User

from courses.models import Lesson, LessonStatus


class Study:
    def __init__(self, request):
        self.request = request
        self.lesson_statuses = {}

    def mentee_List(self):
        if self.request.user.is_superuser:
            all_current_mentee = User.objects.filter(profile__current_mentee=True)
        else:
            all_current_mentee = None
        return all_current_mentee

    def list_for_user(self, mentee_id):
        if mentee_id is None:
            list_for_user = self.request.user.id
        else:
            list_for_user = mentee_id
        return list_for_user

    def lessons_list(self, mentee_id, course):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:

                # if superuser look self lesson
                if mentee_id is None:
                    statuses_for_user = self.request.user

                # if superuser look page mentee
                else:
                    statuses_for_user = mentee_id
                self.lessons = Lesson.objects.filter(topic__course__title=course).order_by('topic__grade', 'topic__num_topic', 'num_lesson')
                self.lesson_statuses = LessonStatus.objects.filter(user=statuses_for_user, lesson__in=self.lessons)

            # if user is mentee
            else:
                statuses_for_user = self.request.user
                self.lessons = Lesson.objects.filter(topic__course__title=course).order_by('topic__grade', 'topic__num_topic', 'num_lesson')
                self.lesson_statuses = LessonStatus.objects.filter(user=statuses_for_user, lesson__in=self.lessons)

        # if user not auth
        else:
            self.lessons = Lesson.objects.filter(topic__course__title=course).order_by('topic__grade', 'topic__num_topic', 'num_lesson')


        # add lessons in dict
        lessons_dict = []
        for lesson in self.lessons:
            add = {
                'id': lesson.id,
                'grade': lesson.topic.grade,
                'topic': lesson.topic.title,
                'title': lesson.title,
                'get_absolute_url': lesson.get_absolute_url,
            }
            # add statuses in dict
            for status in self.lesson_statuses:
                if status.lesson.id == lesson.id:
                    add['status'] = status.status
            lessons_dict.append(add)

        return lessons_dict

    def progress(self):
        g1_progress, g2_progress, g3_progress = 0, 0, 0

        if self.request.user.is_anonymous:
            return {'g1_progress': g1_progress, 'g2_progress': g2_progress, 'g3_progress': g3_progress}

        # calculate progress
        lessons_g1 = self.lesson_statuses.filter(lesson__topic__grade=1)
        lessons_g1_done = lessons_g1.filter(status='done')
        lessons_g2 = self.lesson_statuses.filter(lesson__topic__grade=2)
        lessons_g2_done = lessons_g2.filter(status='done')
        lessons_g3 = self.lesson_statuses.filter(lesson__topic__grade=3)
        lessons_g3_done = lessons_g3.filter(status='done')

        try:
            g1_progress = round(len(lessons_g1_done) / (len(lessons_g1) / 100))
            g2_progress = round(len(lessons_g2_done) / (len(lessons_g2) / 100))
            g3_progress = round(len(lessons_g3_done) / (len(lessons_g3) / 100))
        except:
            ...

        return {'g1_progress': g1_progress, 'g2_progress': g2_progress, 'g3_progress': g3_progress}