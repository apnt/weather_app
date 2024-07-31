from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    """Default pagination for all weather_app api viewsets"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000
