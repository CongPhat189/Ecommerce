from rest_framework import pagination


class CoursePagination(pagination.PageNumberPagination):
    page_size = 8
