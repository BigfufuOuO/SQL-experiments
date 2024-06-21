from django.db import models
from django import forms
from django.core.validators import RegexValidator
from Teachers.models import Teacher

# Create your models here.
class Course(models.Model):
    type_choices = [
        (1, '本科生课程'),
        (2, '研究生课程')
    ]
    ID = models.CharField(verbose_name='课程号', max_length=256, primary_key=True)
    name = models.CharField(verbose_name='课程名称', max_length=256)
    hours = models.IntegerField(verbose_name='学时数')
    course_type = models.IntegerField(verbose_name='课程性质', choices=type_choices)
    
    def __str__(self):
        return self.ID + ', ' + self.name + ', ' + str(self.hours) + '学时'
    
class Teacher_Course(models.Model):
    semester_choices = [
        (1, '春季学期'),
        (2, '夏季学期'),
        (3, '秋季学期')
    ]
    
    teacher_ID = models.ForeignKey(to='Teachers.Teacher', to_field='ID', on_delete=models.CASCADE)
    course_ID = models.ForeignKey(to='Course', to_field='ID', on_delete=models.CASCADE)
    semester = models.IntegerField(verbose_name='学期', choices=semester_choices)
    year = models.IntegerField(verbose_name='学年')
    hours_taken = models.IntegerField(verbose_name='承担学时')
    
    class Meta:
        unique_together = ('teacher_ID', 'course_ID', 'year', 'semester')


class CourseForm(forms.ModelForm):
    ID = forms.CharField(label='课程号', max_length=256,
                         validators=[RegexValidator(r'^[a-zA-Z0-9]+$', '必须是字母或数字的组合')],
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    hours = forms.IntegerField(label='学时数', min_value=1,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Course
        fields = ['ID', 'name', 'hours', 'course_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_type': forms.Select(attrs={'class': 'custom-select'}),
        }


class CourseDetailForm(forms.ModelForm):
    course_ID = forms.ModelChoiceField(queryset=Course.objects.all(), label='课程',
                                    widget=forms.Select(attrs={'class': 'course-select form-control'}))
    year = forms.IntegerField(label='年份', min_value=2000, max_value=2024,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Teacher_Course
        fields = ['course_ID', 'year', 'semester']
        widgets = {
            'semester': forms.Select(attrs={'class': 'custom-select'}),
        }

    def clean(self):
        super().clean()
        # 检查该课程是否被添加过
        print(self.cleaned_data)
        course_ID = self.cleaned_data.get('course_ID', None)
        year = self.cleaned_data.get('year', None)
        semester = self.cleaned_data.get('semester', 0)
        if len(str(semester)) == 0:
            semester = None
        # 如果除了自身已存在
        if Teacher_Course.objects.filter(course_ID=course_ID, year=year, semester=semester).exists():
            raise forms.ValidationError('该课程已经被添加过')

    def __init__(self, *args, **kwargs):
        operation_type = kwargs.pop('operation_type', None)
        self.operation_type = operation_type
        super().__init__(*args, **kwargs)
        if operation_type == 'update':
            self.fields['course_ID'].disabled = True
            self.fields['course_ID'].required = False
        elif operation_type == 'query':
            for field in self.fields.values():
                field.required = False

class TeacherCourseForm(forms.ModelForm):
    teacher_ID = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='教师',
                                        widget=forms.Select(attrs={'class': 'teacher-select form-control'}))
    hours_taken = forms.IntegerField(label='承担学时数', min_value=1,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Teacher_Course
        fields = ['teacher_ID', 'hours_taken']

    def __init__(self, *args, **kwargs):
        operation_type = kwargs.pop('operation_type', None)
        self.operation_type = operation_type
        super().__init__(*args, **kwargs)
        if operation_type == 'update':
            self.fields['ID'].readonly = True
        elif operation_type == 'query':
            for field in self.fields.values():
                field.required = False

class TeacherCourseFormSet_custom(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.course_instance = kwargs.pop('course_instance', None)
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
            form.fields['id'].required = False

    def clean(self):
        super().clean()
        # 输出所有数据
        for form in self.forms:
            print(form.cleaned_data)

        if any(self.errors):
            return

        # 作者不能重复
        teachers = []
        for form in self.forms:
            teacher = form.cleaned_data.get('teacher_ID', None)
            if teacher in teachers:
                raise forms.ValidationError('教师不能重复')
            teachers.append(teacher)

        # 时间总和必须等于课程学时
        total_hours = 0
        for form in self.forms:
            total_hours += form.cleaned_data.get('hours_taken', 0)
        course_ID = self.data.get('course_ID', None) or self.course_instance.ID
        course_hours = Course.objects.get(ID=course_ID).hours
        if total_hours != course_hours:
            raise forms.ValidationError('教师承担学时总和必须等于课程学时')

    def save(self, course_info, commit=True):
        for form in self.forms:
            instance = form.save(commit=False)
            instance.course_ID = course_info.course_ID
            instance.year = course_info.year
            instance.semester = course_info.semester
            instance.save()



TeacherCourseFormSet = forms.modelformset_factory(model=Teacher_Course, form=TeacherCourseForm,
                                                  formset=TeacherCourseFormSet_custom, extra=1)
TeacherCourseEditSet = forms.modelformset_factory(model=Teacher_Course, form=TeacherCourseForm,
                                                         extra=0)

