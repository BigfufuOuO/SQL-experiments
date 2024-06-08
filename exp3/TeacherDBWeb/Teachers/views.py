from django.shortcuts import render
from . import models
from .models import TeacherForm

length = [3, 3, 3, 3]

# Create your views here.
def teachermanage(request):
    teacherForm = models.TeacherForm()
    return render(request, 'teachermanage.html', 
                  {'teacherForm': teacherForm, 'length': length})

def teacher_search(request):
    if request.method == "GET":
        form = TeacherForm(request.GET)
        print(form)
    teachers = models.Teacher.objects.all()
    return render(request, 'teacher_search.html',
                  {'teachers': teachers})

def teacher_add(request, id='0'):
    # POST get input and check
    form = TeacherForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        instance = form.save()
        return render(request, 'teacher_add.html',
                      {'teacherForm': instance, 'length': length})
    else:
        return render(request, 'teachermanage.html',
                      {'teacherForm': form, 'length': length})

def teacher_edit(request, id='0'):
    ''' edit teacher'''

    if request.method == "GET":
        # get original data according to id
        original_data = models.Teacher.objects.get(ID=id)
        form = TeacherForm(instance=original_data)
        return render(request, 'teacher_edit.html',
                      {'teacherForm': form, 'length': length})

    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            teachers = models.Teacher.objects.all()
            return render(request, 'teacher_search.html',
                          {'teachers': teachers})
        else:
            return render(request, 'teacher_edit.html',
                      {'teacherForm': form, 'length': length})

