from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
import json
from .models import Teacher_Paper, PaperForm, AuthorForm, AuthorFormSet

length = [6, 6, 4, 3, 3, 3]
# Create your views here.
def paper_manage(request):
    paper_form = PaperForm()
    #author_form_set = modelformset_factory(Teacher_Paper, form=AuthorForm, extra=1)
    author_form_set = AuthorFormSet()
    #print(author_form_set)
    return render(request, 'PaperManage.html',
                  {'paperForm': paper_form, 'authorFormSet': author_form_set,
                   'length': length})

@csrf_exempt
def paper_add(request):
    paper_form = PaperForm(data=request.POST)
    author_form_set = AuthorFormSet(data=request.POST or None)
    print(request.POST)
    if paper_form.is_valid() and author_form_set.is_valid():
        instance_paper = paper_form.save()
        instance_
        data_dic = {"status": True}
        return render(request, 'paper_add.html',
                      {'paperForm': instance_paper})
    else:
        data_dic = {"status": False, "error": [paper_form.errors, author_form_set.errors,
                                               author_form_set.non_form_errors()]}
        return HttpResponse(json.dumps(data_dic))

def paper_search(request):

    pass