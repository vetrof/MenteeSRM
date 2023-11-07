from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from message.models import SpamForAllUsers


@admin.register(SpamForAllUsers)
class SpamForAllUsersAdmin(SummernoteModelAdmin):
    list_display = ['id', 'subject']
    summernote_fields = '__all__'




