from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

class PageNumberPagination(PageNumberPagination):
    def get_first_link(self):
        url = self.request.build_absolute_uri()
        page_number = 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginator(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)
    
    def get_pages(self):
        url = self.request.build_absolute_uri()
        return [
            {
                'index': page_number,
                'url': replace_query_param(url, self.page_query_param, page_number)
            }
            for page_number in self.page.paginator.page_range 
        ]

class Paginator(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'first': self.get_first_link(),
                'last': self.get_last_link(),
                'pages': self.get_pages(),
            },
            'index': self.page.number,
            'count': self.page.paginator.count,
            'datas': data,
        })