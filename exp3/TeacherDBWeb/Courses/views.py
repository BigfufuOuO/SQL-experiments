from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from Teachers.tools.Page import Pageination
import json

# Create your views here.
@csrf_exempt
def course_add_individually(request):
    if request.method == 'GET':
        course_form = CourseForm()
        return render(request, 'course_add.html',
                      {'courseForm': course_form})

    if request.method == 'POST':
        course_form = CourseForm(data=request.POST)
        if course_form.is_valid():
            course_form.save()
            data_dic = {"status": True, "error": []}
            return HttpResponse(json.dumps(data_dic))
        else:
            data_dic = {"status": False,
                        "error": {'courseForm error':course_form.errors}}
            return HttpResponse(json.dumps(data_dic))

def course_manage(request):
    course_form = CourseDetailForm()
    teacher_course_formset = TeacherCourseFormSet(queryset=Teacher_Course.objects.none())
    return render(request, 'course_manage.html',
                  {'courseForm': course_form,
                   'teacherFormSet': teacher_course_formset})


@csrf_exempt
def course_add(request):
    course_form = CourseDetailForm(data=request.POST)
    teacher_course_formset = TeacherCourseFormSet(data=request.POST)
    if course_form.is_valid() and teacher_course_formset.is_valid():
        # save data
        course_info = course_form.save(commit=False)
        #print(course_info.__dict__)
        teacher_course_formset = teacher_course_formset.save(course_info=course_info)
        data_dic = {"status": True, "error": []}
        return HttpResponse(json.dumps(data_dic))
        pass
    else:
        # return error messages
        data_dic = {"status": False,
                    "error": {'courseForm error': course_form.errors,
                              'teacherForms error': teacher_course_formset.errors,
                              'teacherFormSet error': teacher_course_formset.non_form_errors()}}
        return HttpResponse(json.dumps(data_dic))

def course_search(request):
    course_form = CourseDetailForm(data=request.GET, operation_type='query')
    data_dict = {}
    for field in course_form.fields:
        data = request.GET.get(field, None)
        if data:
            data_dict[field] = data
    teachers = Teacher_Course.objects.filter(**data_dict).select_related('course_ID', 'teacher_ID')
    courses = {teacher.course_ID for teacher in teachers}
    itemCount = teachers.count()
    print(courses, teachers, itemCount)

    # page
    page = Pageination(request, itemCount)
    teachers = teachers[(page.pageInfo['pageNowInt'] - 1) * 10: page.pageInfo['pageNowInt'] * 10]


    return render(request, 'course_search.html',
                  {'courseForm': course_form,
                   'teachers': teachers,
                   'courses': courses,
                   'page_list': page.page_list, 'pageInfo': page.pageInfo})

    pass

@csrf_exempt
def course_edit(request, id='0', year=2000, semester=1):
    original_course = Course.objects.get(ID=id)
    if request.method == 'GET':
        course_form = CourseDetailForm(operation_type='update')
        course_teacher_data = list(Teacher_Course.objects.filter(course_ID=id, year=year, semester=semester).values())
        print(course_teacher_data)
        teacher_course_formset = TeacherCourseEditSet(queryset=Teacher_Course.objects.filter(course_ID=id, year=year, semester=semester))
        print(len(teacher_course_formset))
        for i, form in enumerate(teacher_course_formset):
            form.initial = {'teacher_ID': course_teacher_data[i]['teacher_ID_id'],
                            'hours_taken': course_teacher_data[i]['hours_taken']}
        course_form.initial = {'course_ID': id, 'year': year, 'semester': semester}
        return render(request, 'course_edit.html',
                        {'courseForm': course_form,
                         'teacherFormSet': teacher_course_formset})

    if request.method == 'POST':
        course_form = CourseDetailForm(data=request.POST, operation_type='update')
        teacher_course_formset = TeacherCourseFormSet(data=request.POST, course_instance=original_course)
        if course_form.is_valid() and teacher_course_formset.is_valid():
            course_info = course_form.save(commit=False)
            course_info.course_ID = original_course
            # 原数据
            original_teacher_course_data = Teacher_Course.objects.filter(course_ID=id, year=year, semester=semester)
            # 删除
            for data in original_teacher_course_data:
                data.delete()
            # 新数据
            teacher_course_formset = teacher_course_formset.save(course_info=course_info)
            data_dic = {"status": True, "error": []}
            return HttpResponse(json.dumps(data_dic))
            pass
        else:
            # return error messages
            data_dic = {"status": False,
                        "error": {'courseForm error': course_form.errors,
                                  'teacherForms error': teacher_course_formset.errors,
                                  'teacherFormSet error': teacher_course_formset.non_form_errors()}}
            return HttpResponse(json.dumps(data_dic))

def course_delete(request, id='0', year=2000, semester=1):
    teacher_course_data = Teacher_Course.objects.filter(course_ID=id, year=year, semester=semester)
    teacher_course_data.delete()
    return redirect('/courses/search/')

