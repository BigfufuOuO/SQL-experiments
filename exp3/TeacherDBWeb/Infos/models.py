from django.db import models

# Create your models here.
from django.db import models
from django import forms
from django.core.validators import RegexValidator
from Teachers.models import Teacher

class TeacherInfo(forms.ModelForm):
    ID_spec = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='教师',
                                widget=forms.Select(attrs={'class': 'teacher-select form-control'}))

    start_year = forms.IntegerField(label='起始年份', min_value=2000, max_value=2024,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))

    end_year = forms.IntegerField(label='结束年份', min_value=2000, max_value=2024,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Teacher
        fields = ['ID_spec', 'start_year', 'end_year']

    def clean(self):
        super().clean()
        # 输出数据
        print(self.cleaned_data)
        if any(self.errors):
            return

        # 检查年份
        start_year = self.cleaned_data.get('start_year')
        end_year = self.cleaned_data.get('end_year')
        if start_year > end_year:
            raise forms.ValidationError('起始年份不能大于结束年份')
