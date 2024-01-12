from rest_framework.pagination import PageNumberPagination

from foodgram.constants import PAGE_PAGINATION_NUMBER


class CustomPaginator(PageNumberPagination):
    """Собственный пагинатор."""
    page_size = PAGE_PAGINATION_NUMBER
    page_size_query_param = 'limit'
