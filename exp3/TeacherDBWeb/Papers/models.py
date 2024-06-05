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
    
    ID = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    source = models.CharField(max_length=256)
    publish_date = models.DateField()
    publish_type = models.IntegerField(choices=type_choices)
    publish_level = models.IntegerField(choices=level_choices)
    
    def __str__(self):
        return self.ID
    
# TEACHER_PAPER
class Teacher_Paper(models.Model):
    teacher = models.ForeignKey('Teachers.Teacher', on_delete=models.CASCADE)
    paper = models.ForeignKey('Papers.Paper', on_delete=models.CASCADE)
    rank = models.IntegerField()
    is_corresponding_author = models.BooleanField()
    
    class Meta:
        unique_together = ('teacher', 'paper')
        
    def __str__(self):
        return self.teacher.ID + ' ' + self.paper.ID