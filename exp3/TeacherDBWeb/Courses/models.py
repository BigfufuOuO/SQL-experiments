from django.db import models

# Create your models here.
class Course(models.Model):
    type_choices = [
        (1, '本科生课程'),
        (2, '研究生课程')
    ]
    ID = models.CharField(max_length=256, primary_key=True)
    name = models.CharField(max_length=256)
    hours = models.IntegerField()
    course_type = models.IntegerField(choices=type_choices)
    
    def __str__(self):
        return self.ID
    
class Teacher_Course(models.Model):
    semester_choices = [
        (1, '春季学期'),
        (2, '夏季学期'),
        (3, '秋季学期')
    ]
    
    teacher_ID = models.ForeignKey(to='Teachers.Teacher', to_field='ID', on_delete=models.CASCADE)
    course_ID = models.ForeignKey(to='Course', to_field='ID', on_delete=models.CASCADE)
    semester = models.IntegerField()
    year = models.IntegerField()
    hours_taken = models.IntegerField()
    
    class Meta:
        unique_together = ('teacher_ID', 'course_ID')
    
    def __str__(self):
        return self.ID