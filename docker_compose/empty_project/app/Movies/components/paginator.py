from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .DRF import PAGE_SIZE


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_page = 1

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('total_pages', self.total_pages),
            ('next', self.next),
            ('prev', self.prev),
            ('results', data)
        ]))

    @property
    def prev(self):
        value = None if self.page < 2 else self.page - 1
        return value

    @property
    def next(self):
        if self.count == 0:
            return None
        value = None if self.page == self.total_pages else self.page + 1
        return value

    def get_page(self):
        page = self.request.query_params.get('page')
        if page:
            if page == 'last':
                return self.total_pages
            try:
                return int(page)
            except ValueError:
                pass
        return self.default_page

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        self.total_pages = self.get_total_pages(self.count)
        self.request = request
        self.page = self.get_page()
        if self.count == 0:
            return []

        if self.page == self.default_page:
            results = list(queryset[:PAGE_SIZE])
        elif self.page == self.total_pages:
            start = self.count - (self.count % PAGE_SIZE)
            results = list(queryset[start:])
        else:
            start = PAGE_SIZE * (self.page - 1)
            finish = start + PAGE_SIZE
            results = list(queryset[start:finish])
        return results

    @staticmethod
    def get_total_pages(value: int) -> int:
        pages = 0 if value == 0 else value // PAGE_SIZE + 1
        return pages
