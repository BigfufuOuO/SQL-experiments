from django.shortcuts import render, redirect
from . import models
from .models import TeacherForm
from .tools.Page import Pageination


length = [3, 3, 3, 3]

# Create your views here.
def teachermanage(request):
    teacherForm = models.TeacherForm()
    return render(request, 'teachermanage.html', 
                  {'teacherForm': teacherForm, 'length': length})

def teacher_search(request):
    form = TeacherForm(data=request.GET, operation_type='query')
    data_dict = {}
    for field in form.fields:
        data = request.GET.get(field, '')
        if data:
            data_dict[field] = data

    teachers = models.Teacher.objects.filter(**data_dict)
    itemCount = teachers.count()
    print(teachers, itemCount)

    # page
    page = Pageination(request, itemCount)
    teachers = teachers[(page.pageInfo['pageNowInt'] - 1) * 10: page.pageInfo['pageNowInt'] * 10]

    # delete unique error
    if form.has_error('ID', code='unique'):
        del form.errors['ID']


    return render(request, 'teacher_search.html',
                  {'teacherForm': form,
                   'teachers': teachers,
                   'page_list': page.page_list, 'pageInfo': page.pageInfo})

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
        form = TeacherForm(instance=original_data, operation_type='update')
        return render(request, 'teacher_edit.html',
                      {'teacherForm': form, 'length': length})

    original_data = models.Teacher.objects.get(ID=id)
    if request.method == "POST":
        form = TeacherForm(data=request.POST, instance=original_data, operation_type='update') # 防止编辑新建
        if form.is_valid():
            form.save()
            teachers = models.Teacher.objects.all()
            return redirect('/teachers/search/')
        else:
            return render(request, 'teacher_edit.html',
                      {'teacherForm': form, 'length': length})

def teacher_delete(request, id='0'):
    models.Teacher.objects.get(ID=id).delete()
    return redirect('/teachers/search/')
    pass

