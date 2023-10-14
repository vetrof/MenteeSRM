from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Course(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Grade(models.Model):
    level = models.IntegerField()
    info = models.TextField(blank=True)

    def __str__(self):
        return str(self.level)


class Topic(models.Model):
    title = models.CharField(max_length=200)
    num_topic = models.FloatField()
    info = models.TextField(blank=True)

    def __str__(self):
        return f'{self.num_topic} | {self.title}'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    num_lesson = models.FloatField()
    title = models.CharField(max_length=300)
    info = models.TextField(blank=True)

    def __str__(self):
        return self.title


class LessonStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('not_started', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('to_repeat', 'Повторить'),
        ('done', 'Закончено'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return f'{self.user.username} - {self.lesson.title} - {self.get_status_display()}'


# Создаем сигнал, который будет создавать LessonStatus при создании урока
@receiver(post_save, sender=Lesson)
def create_lesson_status(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        for user in users:
            LessonStatus.objects.create(user=user, lesson=instance)


@receiver(post_save, sender=User)
def create_lesson_statuses_for_new_user(sender, instance, created, **kwargs):
    if created:
        lessons = Lesson.objects.all()
        for lesson in lessons:
            LessonStatus.objects.get_or_create(user=instance, lesson=lesson)
