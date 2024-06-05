from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    name = 'Django'
    return render(request, 'hh.html', {'name': name})