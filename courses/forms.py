from django import forms

from courses.models import Notes, Question


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['info']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['client_info']
