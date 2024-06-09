'''
分页组件
'''
import copy
from django.utils.safestring import mark_safe
class Pageination:

    def __init__(self, request, itemsCount, pageParam='page'):
        """
        :param request: 请求头
        :param itemsCount: item数量
        :param pageParam: page名称
        """
        pageNow = int(request.GET.get('page', 1))
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        query_dict.setlist('page', [pageNow])


        # prev, next
        if pageNow - 1 < 1:
            prev = mark_safe(f'<a class="page-link">Previous</a>')
        else:
            query_dict.setlist('page', [pageNow - 1])
            prev = mark_safe(f'<a class="page-link" href="?{query_dict.urlencode()}">Previous</a>')

        if pageNow + 1 > itemsCount // 10 + 1:
            next = mark_safe(f'<a class="page-link">Next</a>')
        else:
            query_dict.setlist('page', [pageNow + 1])
            next = mark_safe(f'<a class="page-link" href="?{query_dict.urlencode()}">Next</a>')

        self.pageInfo = {
            'pageNowInt': pageNow,
            'pagePrev': prev,
            'pageNext': next,
            'pageCount': itemsCount // 10 + 1
        }

        # pages list
        self.page_list = []
        for i in range(1, itemsCount // 10 + 2):
            if i > pageNow - 3 and i < pageNow + 3:
                query_dict.setlist('page', [i])
                if i == pageNow:
                    element = f'<li class="page-item active"><a class="page-link" href="?{query_dict.urlencode()}">{i}</a></li>'
                else:
                    element = f'<li class="page-item"><a class="page-link" href="?{query_dict.urlencode()}">{i}</a></li>'
                self.page_list.append(element)
        self.page_list = mark_safe(''.join(self.page_list))