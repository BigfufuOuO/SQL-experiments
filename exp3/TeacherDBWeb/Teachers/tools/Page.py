'''
分页组件
'''
class Pageination:

    def __init__(self, request, itemsCount, pageParam='page'):
        pageNow = int(request.GET.get('page', 1))
        self.pageInfo = {'pageNow': pageNow, 'pagePrev': pageNow - 1, 'pageNext': pageNow + 1}

        # pages list
        self.page_list = []
        for i in range(1, itemsCount // 10 + 2):
            if i > pageNow - 3 and i < pageNow + 3:
                self.page_list.append(i)