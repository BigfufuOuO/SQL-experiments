from django.db import models

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
    
    def __str__(self):
        return self.ID
    
# TEACHER_PAPER
class Teacher_Paper(models.Model):
    teacher = models.ForeignKey(to='Teachers.Teacher', to_field='ID', on_delete=models.CASCADE)
    paper = models.ForeignKey(to='Paper', to_field='ID', on_delete=models.CASCADE)
    rank = models.IntegerField()
    is_corresponding_author = models.BooleanField()
    
    class Meta:
        unique_together = ('teacher', 'paper')
        
    def __str__(self):
        return self.teacher.ID + ' ' + self.paper.ID