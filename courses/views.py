from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from courses.forms import NotesForm, QuestionForm
from courses.models import Lesson, Notes


def index_page(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()


    form = QuestionForm()
    return render(request, 'index.html')


def contacts_page(request):
    return render(request, 'contacts.html')


def helpers_page(request):
    return render(request, 'helpers.html')


@login_required
def lesson_detail(request, id):
    lesson = Lesson.objects.get(id=id)
    return render(request, 'lesson_detail.html', {'lesson': lesson})


@login_required
def calendar(request):
    return render(request, 'calendar.html')


@login_required
def edit_note(request, id):
    note = Notes.objects.get(id=id)
    if request.user != note.user:
        # Защита от редактирования чужих записок
        return redirect('sticky_wall')

    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('sticky_wall')
    else:
        form = NotesForm(instance=note)

    return render(request, 'sticky_wall.html', {'form': form})


@login_required
def sticky_wall(request):
    notes = Notes.objects.filter(user=request.user).order_by('-id')

    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.author = request.user
            note.save()
            return redirect('sticky_wall')
    else:
        form = NotesForm()

    return render(request, 'sticky_wall.html', {'notes': notes, 'form': form})