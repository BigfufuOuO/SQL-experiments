from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
import json
from .models import Paper, Teacher_Paper, PaperForm, AuthorForm, AuthorFormSet
from Teachers.tools.Page import Pageination

length = [6, 6, 4, 3, 3, 3]
# Create your views here.
def paper_manage(request):
    paper_form = PaperForm()
    #author_form_set = modelformset_factory(Teacher_Paper, form=AuthorForm, extra=1)
    author_form_set = AuthorFormSet(queryset=Teacher_Paper.objects.none())
    # print(author_form_set)
    return render(request, 'PaperManage.html',
                  {'paperForm': paper_form, 'authorFormSet': author_form_set,
                   'length': length})

@csrf_exempt
def paper_add(request):
    paper_form = PaperForm(data=request.POST)
    author_form_set = AuthorFormSet(data=request.POST or None)
    print(request.POST)
    print(author_form_set.data.get('ID'))
    if paper_form.is_valid() and author_form_set.is_valid():
        instance_paper = paper_form.save()
        instance_author = author_form_set.save(commit=False)
        data_dic = {"status": True, "error": []}
        return HttpResponse(json.dumps(data_dic))
    else:
        data_dic = {"status": False, "error": [paper_form.errors, author_form_set.errors,
                                               author_form_set.non_form_errors()]}
        return HttpResponse(json.dumps(data_dic))

@csrf_exempt
def paper_search(request):
    paper_form = PaperForm(data=request.GET, operation_type='query')
    print(request.GET)
    data_dict = {}
    for field in paper_form.fields:
        data = request.GET.get(field, '')
        if data:
            data_dict[field] = data

    papers = Paper.objects.filter(**data_dict)
    itemCount = papers.count()
    print(papers, itemCount)

    # page
    page = Pageination(request, itemCount)
    papers = papers[(page.pageInfo['pageNowInt'] - 1) * 10: page.pageInfo['pageNowInt'] * 10]

    # delete unique error
    if paper_form.has_error('ID', code='unique'):
        del paper_form.errors['ID']

    return render(request, 'paper_search.html',
                  {'paperForm': paper_form,
                   'papers': papers,
                   'page_list': page.page_list, 'pageInfo': page.pageInfo})
    pass