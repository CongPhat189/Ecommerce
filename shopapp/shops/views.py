from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from shops import serializers, paginators
from shops.models import Category, Shop, Product, User


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
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

        return Response(serializers.ProductSerializer(products, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset =  Product.objects.filter(active=True).all()
    serializer_class = serializers.ProductSerializer

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_name='current_user', detail=False)
    def current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data, status=status.HTTP_200_OK)



