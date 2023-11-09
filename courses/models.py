from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager


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
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    num_topic = models.IntegerField()
    info = models.TextField(blank=True)

    class Meta:
        ordering = ['num_topic']

    def __str__(self):
        course = self.course
        course_short = str(course)[0]
        return f'{course_short}{self.grade.level} {self.num_topic} - {self.title}'


class Lesson(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    num_lesson = models.IntegerField()
    title = models.CharField(max_length=300)
    info = models.TextField(blank=True)
    info_hide = models.TextField(blank=True)
    tags = TaggableManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson_detail', args=[str(self.id)])


class LessonStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('not_started', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('to_repeat', 'Повторить'),
        ('next', 'Следущее'),
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


class Notes(models.Model):
    info = MarkdownxField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    on_top = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"

    def formatted_markdown(self):
        return markdownify(self.info)


class Question(models.Model):
    date = models.DateTimeField(auto_now=True)
    client_info = models.TextField()
    text = models.TextField(blank=True)
