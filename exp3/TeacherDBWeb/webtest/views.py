from django.shortcuts import render
from django.http import HttpResponse

from Teachers.models import Teacher

# Create your views here.
def index(request):
    teacher_list = Teacher.objects.all()
    return render(request, 'hh.html', 
                  {'teacher_list': teacher_list})