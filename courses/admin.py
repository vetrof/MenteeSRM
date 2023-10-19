from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from django_summernote.admin import SummernoteModelAdmin

from courses.models import Lesson, Topic, Grade, Course, LessonStatus, Notes, Question


class LessonTextEditAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'


def copy_selected_items(modeladmin, request, queryset):
    for item in queryset:
        item.pk = None  # Сбрасываем первичный ключ, чтобы создать новую запись
        item.save()
    copy_selected_items.short_description = "Копировать выбранные записи"


# @admin.register(Lesson)
# class LessonAdmin(admin.ModelAdmin):
#     list_display = ['id','course', 'grade', 'num_topic', 'topic', 'num_lesson', 'title']
#     list_display_links = ['topic', 'num_lesson', 'title']
#     ordering = ['grade', 'topic__num_topic', 'num_lesson', 'id']
#     actions = [copy_selected_items]
#     list_filter = ['grade', 'topic']

@admin.register(Lesson)
class LessonAdmin(SummernoteModelAdmin):
    list_display = ['id', 'course', 'grade', 'num_topic', 'topic', 'num_lesson', 'title']
    list_display_links = ['topic', 'num_lesson', 'title']
    ordering = ['grade', 'topic__num_topic', 'num_lesson', 'id']
    actions = [copy_selected_items]
    list_filter = ['grade', 'topic']
    summernote_fields = '__all__'


    def num_topic(self, obj):
        return obj.topic.num_topic

    num_topic.short_description = 'Topic Number'


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ['author', 'user', 'date']
    list_filter = ['user']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'client_info']


admin.site.register(Course)
admin.site.register(Grade)
admin.site.register(Topic, LessonTextEditAdmin)
admin.site.register(LessonStatus)



