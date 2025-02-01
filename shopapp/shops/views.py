from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from shops import serializers, paginators
from shops.models import Category,Shop




class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset =  Category.objects.all()
    serializer_class = serializers.CategorySerializer

class ShopViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Shop.objects.filter(active=True).all()
    serializer_class = serializers.ShopSerializer
    pagination_class = paginators.ShopPaginator


    def get_queryset(self):
        queries = self.queryset
        cate_id = self.request.query_params.get('cate_id')
        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(shop_name__icontains=q)

        if cate_id:
            queries = queries.filter(category_id=cate_id)
        return queries


    @action(detail=True, methods=['get'])
    def products(self, request, pk):
        products = self.get_object().product_set.filter(active=True).all()


        return Response(serializers.ProductSerializer(products, many=True, context={'request': request}).data, status= status.HTTP_400_BAD_REQUEST)










