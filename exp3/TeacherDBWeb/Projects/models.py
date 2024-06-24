from django.db import models
from django import forms
from django.core.validators import RegexValidator
from Teachers.models import Teacher

# Create your models here.
class Project(models.Model):
    type_choices = [
        (1, '国家级项目'),
        (2, '省部级项目'),
        (3, '市厅级项目'),
        (4, '企业合作项目'),
        (5, '其他')
    ]
    
    ID = models.CharField(verbose_name='项目号', max_length=256, primary_key=True)
    name = models.CharField(verbose_name='项目名称', max_length=256)
    source = models.CharField(verbose_name='项目来源', max_length=256)
    project_type = models.IntegerField(verbose_name='项目类型', choices=type_choices)
    fund = models.FloatField(verbose_name='总经费')
    start_date = models.IntegerField(verbose_name='开始年份')
    end_date = models.IntegerField(verbose_name='结束年份')
    
    def __str__(self):
        return self.ID
    
class Teacher_Project(models.Model):
    teacher_ID = models.ForeignKey(verbose_name='教师', to='Teachers.Teacher', to_field='ID', on_delete=models.CASCADE) # ForeignKey 级联删除
    project_ID = models.ForeignKey(verbose_name='项目', to='Project', to_field='ID', on_delete=models.CASCADE) # ForeignKey 级联删除
    rank = models.IntegerField(verbose_name='排名')
    fund_taken = models.FloatField(verbose_name='承担经费')
    
    class Meta:
        unique_together = ('teacher_ID', 'project_ID')
    


class ProjectForm(forms.ModelForm):
    ID = forms.CharField(label='项目号', max_length=256,
                         validators=[RegexValidator(r'^[a-zA-Z0-9]+$', '必须是字母或数字的组合')],
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date = forms.IntegerField(label='开始年份', min_value=2000, max_value=2024,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    end_date = forms.IntegerField(label='结束年份', min_value=2000,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Project
        fields = ['ID', 'name', 'source', 'project_type', 'start_date', 'end_date']
        widgets = {
            #'ID': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'project_type': forms.Select(attrs={'class': 'custom-select'}),
            #'start_date': forms.DateInput(attrs={'class': 'form-control'}),
            #'end_date': forms.DateInput(attrs={'class': 'form-control'}),
        }

    def save(self, sum_funds, commit=True):
        instance = super().save(commit=False)
        instance.fund = sum_funds
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        operation_type = kwargs.pop('operation_type', None)
        self.operation_type = operation_type
        super().__init__(*args, **kwargs)
        if operation_type == 'update':
            self.fields['ID'].disabled = True
        elif operation_type == 'query':
            for field in self.fields.values():
                field.required = False


class TeacherProjectForm(forms.ModelForm):
    teacher_ID = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='教师',
                                        widget=forms.Select(attrs={'class': 'teacher-select form-control'}))
    rank = forms.IntegerField(label='排名', min_value=1,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Teacher_Project
        fields = ['teacher_ID', 'rank', 'fund_taken']
        widgets = {
            #'teacher_ID': forms.Select(attrs={'class': 'custom-select'}),
            #'project_ID': forms.Select(attrs={'class': 'custom-select'}),
            'rank': forms.TextInput(attrs={'class': 'form-control'}),
            'fund_taken': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TeacherPJFromSet_custom(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
            form.fields['id'].required = False


    def clean(self):
        '''
        检查是否有重复的教师, 排名是否重复.
        :return:
        '''
        super().clean()
        # 输出所有数据
        for form in self.forms:
            print(form.cleaned_data)

        if any(self.errors):
            return

        # 教师不能为空
        for form in self.forms:
            if not form.cleaned_data.get('teacher_ID', None):
                raise forms.ValidationError('教师不能为空')

        # 教师不能重复
        teacher_list = []
        for form in self.forms:
            teacher = form.cleaned_data.get('teacher_ID', None)
            if teacher in teacher_list:
                raise forms.ValidationError('教师不能重复')
            teacher_list.append(teacher)

        # 排名不能重复
        rank_list = []
        for form in self.forms:
            rank = form.cleaned_data.get('rank', None)
            if rank in rank_list:
                raise forms.ValidationError('排名不能重复')
            rank_list.append(rank)


    def save(self, commit=True, project_id='0'):
        '''
        保存数据
        :param commit:
        :return:
        '''
        # 保存数据
        for form in self.forms:
            instance = form.save(commit=False)
            project_ID = self.data.get('ID') or project_id
            instance.project_ID = Project.objects.get(ID=project_ID)
            instance.save()


TeacherPJFormSet = forms.modelformset_factory(model=Teacher_Project, form=TeacherProjectForm,
                                              formset=TeacherPJFromSet_custom, extra=1)

TeacherPJEditSet = forms.modelformset_factory(model=Teacher_Project, form=TeacherProjectForm, extra=0)