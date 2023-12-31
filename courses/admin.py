from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from django.conf import settings
from django.contrib.auth.models import User
from courses.models import Lesson, Topic, Grade, Course, LessonStatus, Notes, Question



class LessonTextEditAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'


def copy_selected_items(modeladmin, request, queryset):
    for item in queryset:
        item.pk = None  # Сбрасываем первичный ключ, чтобы создать новую запись
        item.save()
    copy_selected_items.short_description = "Копировать выбранные записи"


@admin.register(Lesson)
class LessonAdmin(SummernoteModelAdmin):
    list_display = ['topic_course', 'topic_grade', 'num_topic', 'topic_title', 'num_lesson', 'title']
    list_display_links = ['title']
    ordering = ['topic__course', 'topic__grade', 'topic__num_topic', 'num_lesson']
    actions = [copy_selected_items]
    list_filter = ['topic__course', 'topic__grade', 'topic', 'tags']
    summernote_fields = '__all__'
    list_editable = ['num_lesson']
    search_fields = ['info', 'title', 'topic__title', 'topic__course__title']

    fieldsets = [
        ('Lesson Info', {
            'fields': ['topic', 'num_lesson', 'title', 'info'],
        }),
        ('Hidden Info', {
            'classes': ('collapse',),
            'fields': ['info_hide'],
        }),
    ]

    def num_topic(self, obj):
        return obj.topic.num_topic

    def topic_title(self, obj):
        return obj.topic.title

    def topic_grade(self, obj):
        return obj.topic.grade

    def topic_course(self, obj):
        return obj.topic.course

    num_topic.short_description = 'Topic Number'


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ['author', 'user', 'date']
    list_filter = ['user__profile__current_mentee', 'user']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # Устанавливаем фильтрацию для поля "пользователь" (user) на тех, у кого установлена галочка "current_mentee"
            kwargs["queryset"] = User.objects.filter(profile__current_mentee=True)
        elif db_field.name == "author" and not request.META["PATH_INFO"].startswith('/admin/notes/notes/add'):
            # Устанавливаем значение "автор" только при редактировании записи, а не при создании
            kwargs["queryset"] = User.objects.filter(pk=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'client_info']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['course', 'grade', 'num_topic', 'title']
    list_display_links = ['title']
    ordering = ['course', 'grade__level', 'num_topic']
    list_editable = ['course', 'grade', 'num_topic']
    list_filter = ['course', 'grade']


admin.site.register(Course)
admin.site.register(Grade)
admin.site.register(LessonStatus)



