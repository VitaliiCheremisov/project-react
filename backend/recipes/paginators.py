from foodgram.constants import PAGE_PAGINATION_NUMBER
from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    """Собственный пагинатор."""
    page_size = PAGE_PAGINATION_NUMBER
    page_size_query_param = 'limit'
