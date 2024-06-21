from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from Teachers.tools.Page import Pageination

length = [3, 6, 4, 3, 3, 3]
def project_manage(request):
    project_form = ProjectForm()
    teacher_project_formset = TeacherPJFormSet(queryset=Teacher_Project.objects.none())
    return render(request, 'project_manage.html',
                  {'projectForm': project_form,
                   'teacherFormSet': teacher_project_formset,
                   'length': length})

def get_sum_funds(teacher_project_formset):
    sum_funds = 0
    for form in teacher_project_formset:
        sum_funds += form.cleaned_data.get('fund_taken', 0)
    return sum_funds

@csrf_exempt
def project_add(request):
    project_form = ProjectForm(data=request.POST)
    teacher_project_formset = TeacherPJFormSet(data=request.POST)
    print(request.POST)
    if project_form.is_valid() and teacher_project_formset.is_valid():
        # save data
        sum_funds = get_sum_funds(teacher_project_formset)
        instance_project = project_form.save(sum_funds=sum_funds)
        teacher_project_formset = teacher_project_formset.save(commit=False)
        data_dic = {"status": True, "error": []}
        return HttpResponse(json.dumps(data_dic))
        pass
    else:
        # return error messages
        data_dic = {"status": False,
                    "error": {'projectForm error': project_form.errors,
                              'teacherForms error': teacher_project_formset.errors,
                              'teacherFormSet error': teacher_project_formset.non_form_errors()}}
        return HttpResponse(json.dumps(data_dic))

def project_search(request):
    project_form = ProjectForm(data=request.GET, operation_type='query')
    print(request.GET)
    data_dict = {}
    for field in project_form.fields:
        data = request.GET.get(field, '')
        if data:
            data_dict[field] = data

    projects = Project.objects.filter(**data_dict)
    itemCount = projects.count()
    print(projects, itemCount)

    # page
    page = Pageination(request, itemCount)
    projects = projects[(page.pageInfo['pageNowInt'] - 1) * 10: page.pageInfo['pageNowInt'] * 10]

    # delete unique error
    if project_form.has_error('ID', code='unique'):
        del project_form.errors['ID']

    return render(request, 'project_search.html',
                  {'projectForm': project_form,
                   'projects': projects,
                   'page_list': page.page_list, 'pageInfo': page.pageInfo})
    pass

@csrf_exempt
def project_edit(request, id='0'):
    original_project_data = Project.objects.get(ID=id)
    if request.method == 'GET':
        project_form = ProjectForm(instance=original_project_data, operation_type='update')
        # 获取初始信息
        data = list(Teacher_Project.objects.filter(project_ID=id).values())
        print(data)
        teacher_project_formset = TeacherPJEditSet(queryset=Teacher_Project.objects.filter(project_ID=id))
        for i, form in enumerate(teacher_project_formset):
            form.initial = {'teacher_ID': data[i]['teacher_ID_id'], 'rank': data[i]['rank'],
                            'fund_taken': data[i]['fund_taken']}
        return render(request, 'project_edit.html',
                      {'projectForm': project_form, 'teacherFormSet': teacher_project_formset})

    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST, instance=original_project_data, operation_type='update')
        teacher_project_formset = TeacherPJFormSet(data=request.POST)
        if project_form.is_valid() and teacher_project_formset.is_valid():
            sum_funds = get_sum_funds(teacher_project_formset)
            instance_project = project_form.save(sum_funds=sum_funds)
            # 原数据
            original_teacher_project_data = Teacher_Project.objects.filter(project_ID=id)
            # 删除
            for data in original_teacher_project_data:
                data.delete()
            # 重新写入
            teacher_project_formset.save(project_id=id)
            data_dic = {"status": True, "error": []}
            return HttpResponse(json.dumps(data_dic))
        else:
            data_dic = {"status": False,
                        "error": {'projectForm error': project_form.errors,
                                  'teacherForms error': teacher_project_formset.errors,
                                  'teacherFormSet error': teacher_project_formset.non_form_errors()}}
            return HttpResponse(json.dumps(data_dic))
    pass

def project_delete(request, id='0'):
    Project.objects.get(ID=id).delete()
    return redirect('/projects/search')
