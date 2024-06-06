from django.db import models

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