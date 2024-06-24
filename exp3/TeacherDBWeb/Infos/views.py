from django.shortcuts import render, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.template.loader import get_template, render_to_string
from wkhtmltopdf.views import PDFTemplateView
from wkhtmltopdf.views import PDFTemplateResponse
from Teachers.models import Teacher
from Papers.models import Paper, Teacher_Paper
from Projects.models import Project, Teacher_Project
from Courses.models import Course, Teacher_Course
import json

# Create your views here.
def info_index(request):
    info_form = TeacherInfo()
    return render(request, 'info_search.html', {'infoForm': info_form})

def get_teacher_result(teacher, start_year, end_year):
    # 教师基本信息
    teacher_info = Teacher.objects.get(ID=teacher.ID)
    # 教学情况
    teacher_courses = Teacher_Course.objects.filter(Q(teacher_ID=teacher) \
                                                    & Q(year__gte=start_year) & Q(year__lte=end_year)).select_related(
        'course_ID')
    # 科研情况
    teacher_papers = Teacher_Paper.objects.filter(teacher=teacher).select_related('paper')
    teacher_papers = teacher_papers.filter(Q(paper__publish_date__year__gte=start_year)
                                           & Q(paper__publish_date__year__lte=end_year))
    # 项目情况
    teacher_projects = Teacher_Project.objects.filter(teacher_ID=teacher).select_related('project_ID')
    teacher_projects = teacher_projects.filter(Q(project_ID__start_date__gte=start_year)
                                               | Q(project_ID__end_date__lte=end_year))
    print(teacher_info, teacher_courses, teacher_papers, teacher_projects)
    return  teacher_info, teacher_courses, teacher_papers, teacher_projects

@csrf_exempt
def info_search(request):
    if request.method == 'POST':
        info_form = TeacherInfo(data=request.POST)
        if info_form.is_valid():
            # 查找该教师的相关信息
            teacher = info_form.cleaned_data.get('ID_spec')
            start_year = info_form.cleaned_data.get('start_year')
            end_year = info_form.cleaned_data.get('end_year')

            teacher_info, teacher_courses, teacher_papers, teacher_projects = get_teacher_result(teacher, start_year, end_year)
            return render(request, 'info_result.html',
                          {'infoForm': info_form,
                           'teacher': teacher_info, 'teacher_courses': teacher_courses,
                           'teacher_papers': teacher_papers, 'teacher_projects': teacher_projects})
        else:
            form_error = info_form.errors.get('__all__', None)
            return render(request, 'info_search.html',
                          {'infoForm': info_form, 'infoForm_error': form_error})
    else:
        return info_pdf(request)

@csrf_exempt
def info_pdf(request):
    teacher = request.GET.get('ID_spec')
    teacher = Teacher.objects.get(ID=teacher)
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')
    # 信息
    teacher_info, teacher_courses, teacher_papers, teacher_projects = get_teacher_result(teacher, start_year, end_year)
    # 生成html
    teamplate_path = 'result_raw.html'
    template = get_template(teamplate_path)
    html_string = render_to_string('result_raw.html', {'teacher': teacher_info, 'teacher_courses': teacher_courses,
                            'teacher_papers': teacher_papers, 'teacher_projects': teacher_projects})


    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="result.pdf"'
    # PDFTemplateView.as_view(template_name='result_raw.html')(request).render_to_response(response)
    response = PDFTemplateResponse(request=request,
                                      template=teamplate_path,
                                      filename='result.pdf',
                                      context={'teacher': teacher_info, 'teacher_courses': teacher_courses,
                                              'teacher_papers': teacher_papers, 'teacher_projects': teacher_projects},
                                   show_content_in_browser=False)

    return response


