from django.shortcuts import render

# Create your views here.
def paper_manage(request):
    return render(request, 'PaperManage.html')