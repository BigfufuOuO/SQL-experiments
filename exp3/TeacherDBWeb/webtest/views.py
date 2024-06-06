from django.shortcuts import render
from django.http import HttpResponse

from Teachers.models import Teacher

# Create your views here.
def index(request):
    return render(request, 'main.html')