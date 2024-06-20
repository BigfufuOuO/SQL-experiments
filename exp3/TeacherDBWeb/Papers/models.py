from django.db import models
from django import forms
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Teachers.models import Teacher
# Create your models here.
class Paper(models.Model):
    type_choices = [
        (1, 'Full Paper'),
        (2, 'Short Paper'),
        (3, 'Poster Paper'),
        (4, 'Demo Paper')
    ]
    level_choices = [
        (1, 'CCF-A'),
        (2, 'CCF-B'),
        (3, 'CCF-C'),
        (4, '中文CCF-A'),
        (5, '中文CCF-B'),
        (6, '无级别')
    ]
    
    ID = models.IntegerField(primary_key=True, verbose_name="论文序号")
    title = models.CharField(max_length=256, verbose_name="论文名称")
    source = models.CharField(max_length=256, verbose_name="来源")
    publish_date = models.DateField(verbose_name="发表日期")
    publish_type = models.IntegerField(choices=type_choices, verbose_name="类型")
    publish_level = models.IntegerField(choices=level_choices, verbose_name="级别")
    
    # def __str__(self):
    #     return self.ID
    
# TEACHER_PAPER
class Teacher_Paper(models.Model):
    corresponding_author_choices = [
        (1, '是'), (0, '否')
    ]
    teacher = models.ForeignKey(to='Teachers.Teacher', to_field='ID', on_delete=models.CASCADE)
    paper = models.ForeignKey(to='Paper', to_field='ID', on_delete=models.CASCADE)
    rank = models.IntegerField(verbose_name='排名')
    is_corresponding_author = models.BooleanField(choices=corresponding_author_choices, default=0,
                                                  verbose_name='是否通讯作者')
    
    class Meta:
        unique_together = ('teacher', 'paper')
        
    # def __str__(self):
    #     return self.teacher.ID + ' ' + self.paper.ID


# Paper ModelForm
class PaperForm(forms.ModelForm):
    def clean_ID(self):
        str_ID = str(self.cleaned_data['ID'])
        if len(str_ID) != 5:
            raise forms.ValidationError('ID长度必须为5')
        return str_ID
    class Meta:
        model = Paper
        fields = ['ID', 'title', 'source', 'publish_date', 'publish_type', 'publish_level']
        widgets = {
            'ID': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'publish_date': forms.DateInput(attrs={'class': 'form-control'}),
            'publish_type': forms.Select(attrs={'class': 'custom-select'}),
            'publish_level': forms.Select(attrs={'class': 'custom-select'})
        }

    def __init__(self, *args, **kwargs):
        operation_type = kwargs.pop('operation_type', None)
        self.operation_type = operation_type
        super(PaperForm, self).__init__(*args, **kwargs)
        if operation_type == 'update':
            self.fields['ID'].disabled = True
        elif operation_type == 'query':
            for field in self.fields.values():
                field.required = False



class AuthorForm(forms.ModelForm):
    teachers = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='作者',
                                     widget=forms.Select(attrs={'class': 'author-select form-control',}))
    rank = forms.IntegerField(min_value=1, label='排名',
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Teacher_Paper
        fields = ['teachers', 'rank', 'is_corresponding_author']
        widgets = {
            # 'authors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            # 'rank': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_corresponding_author': forms.Select(attrs={'class': 'custom-select'})
        }



class AuthorFormSet_custom(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
            form.fields['id'].required = False

    def clean(self):
        super().clean()
        # 输出所有数据
        for form in self.forms:
            print(form.cleaned_data)

        # 作者不能为空
        for form in self.forms:
            if not form.cleaned_data.get('teachers', None):
                raise forms.ValidationError('作者不能为空')

        if any(self.errors):
            return

        # 作者不能重复
        authors = []
        for form in self.forms:
            author = form.cleaned_data.get('teachers', None)
            if author in authors:
                raise forms.ValidationError('作者重复')
            authors.append(author)

        # 排名不能重复
        ranks = []
        for form in self.forms:
            rank = form.cleaned_data.get('rank', None)
            if rank in ranks:
                raise forms.ValidationError('排名重复')
            ranks.append(rank)

        # 通讯作者只能有一个
        corresponding_author = []
        num_corresponding_author = 0
        for form in self.forms:
            is_corresponding_author = form.cleaned_data.get('is_corresponding_author', None)
            if is_corresponding_author:
                num_corresponding_author += 1
            corresponding_author.append(is_corresponding_author)
        if num_corresponding_author > 1:
            raise forms.ValidationError('通讯作者只能有一个')

    def save(self, commit=True, paper_id='0'):
        for form in self.forms:
            instance = form.save(commit=False)
            paper_id = self.data.get('ID') or paper_id
            instance.teacher = form.cleaned_data.get('teachers')
            instance.paper = Paper.objects.get(ID=paper_id)
            instance.save()





AuthorFormSet = forms.modelformset_factory(model=Teacher_Paper, form=AuthorForm,
                                           formset=AuthorFormSet_custom, extra=1)

AuthorEditSet = forms.modelformset_factory(model=Teacher_Paper, form=AuthorForm, extra=0)