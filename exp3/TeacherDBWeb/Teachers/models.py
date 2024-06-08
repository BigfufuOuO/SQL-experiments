from django.db import models
from django import forms
from django.core.validators import RegexValidator, ValidationError

# Create your models here.
class Teacher(models.Model):
    sex_choices = [(1, ' 男'), (2, '女')]
    position_choices = [
        (1, '博士后'), (2, '助教'),
        (3, '讲师'), (4, '副教授'),
        (5, '特任教授'), (6, '教授'),
        (7, '助理研究员'), (8, '特任副研究员'),
        (9, '副研究员'), (10, '特任研究员'),
        (11, '研究员')
    ]
    ID = models.CharField(verbose_name='工号', max_length=5, primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=256)
    sex = models.IntegerField(verbose_name='性别', choices=sex_choices)
    position = models.IntegerField(verbose_name='职称', choices=position_choices)
    
    def __str__(self):
        return self.ID
    
    
class TeacherForm(forms.ModelForm):
    ID = forms.CharField(label="工号",
                         validators=[RegexValidator(r'^\d{5}$', '必须是5位数字')],
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    def clean_name(self):
        str_name = self.cleaned_data['name']
        # name must not contain any digit or special character
        # 可以是中文
        if any(map(str.isdigit, str_name)):
            raise forms.ValidationError('姓名不能包含数字')
        if str_name and not str_name.replace(' ', '').isalpha():
            raise forms.ValidationError('姓名不能包含特殊字符')
        return str_name

    # def clean_ID(self):
    #     new_ID = self.cleaned_data['ID']
    #     exist_ID = Teacher.objects.exclude(ID=self.instance).filter(ID=new_ID).exists()
    #     print(exist_ID)
    #     if exist_ID:
    #         raise ValidationError('工号已存在')
    #     return new_ID
    def __init__(self, *args, **kwargs):
        operation_type = kwargs.pop('operation_type', None)
        super(TeacherForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['ID'].disabled = True
        if operation_type == 'query':
            for field in self.fields.values():
                field.required = False
        
    class Meta:
        model = Teacher
        # fields = "__all__"
        fields = ['ID', 'name', 'sex', 'position']
        widgets = {
            # "ID": forms.TextInput(attrs={'class': 'form-control'}),
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "sex": forms.Select(attrs={'class': 'custom-select'}),
            "position": forms.Select(attrs={'class': 'custom-select'}),
        }

