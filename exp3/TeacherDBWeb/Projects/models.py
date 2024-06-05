from django.db import models

# Create your models here.
class Project(models.Model):
    type_choices = [
        (1, '国家级项目'),
        (2, '省部级项目'),
        (3, '市厅级项目'),
        (4, '企业合作项目'),
        (5, '其他')
    ]
    
    ID = models.CharField(max_length=256, primary_key=True)
    name = models.CharField(max_length=256)
    source = models.CharField(max_length=256)
    project_type = models.IntegerField(choices=type_choices)
    fund = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.ID
    
class Teacher_Project(models.Model):
    teacher_ID = models.CharField(max_length=5)
    project_ID = models.CharField(max_length=256)
    rank = models.IntegerField()
    fund_taken = models.FloatField()
    
    class Meta:
        unique_together = ('teacher_ID', 'project_ID')
    
    def __str__(self):
        return self.ID