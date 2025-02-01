from rest_framework.pagination import PageNumberPagination


class ShopPaginator( PageNumberPagination):
    page_size = 1
