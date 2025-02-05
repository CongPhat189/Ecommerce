
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


from shops import serializers, paginators, perms
from shops.models import Category, Shop, Product, User, Comment, Like, Order

from django.db.models import Sum,Count
from datetime import datetime


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

class IsSeller(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.user.is_authenticated and request.user.role == 'seller'

# class ShopRegistrationView(viewsets.ViewSet, generics.CreateAPIView):
#     queryset = Shop.objects.all()
#     serializer_class = serializers.ShopSerializer
#     permission_classes = [IsSeller]
#     parser_classes = [parsers.MultiPartParser]
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)




# class ProductCreateView(viewsets.ViewSet,generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = serializers.ProductSerializer
#     permission_classes = [IsSeller]
#     parser_classes = [parsers.MultiPartParser]
#
#     @action(detail=True, methods=['post'], permission_classes=[IsSeller])
#     def perform_create(self, serializer):
#         shop = self.request.user.shops.first()
#         serializer.save(shop=shop)


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
    queryset = Product.objects.filter(active=True).all()
    serializer_class = serializers.ProductDetailSerializer
    permission_classes = [permissions.AllowAny()]

    def get_permissions(self):
        if self.action.__eq__('add_comment' or 'like'):
            return [permissions.IsAuthenticated()]

        return self.permission_classes

    @action(detail=True, methods=['post'], url_path='comments', url_name='comments')
    def add_comment(self, request, pk):
        c = Comment.objects.create(user=request.user, product=self.get_object(), content=request.data.get('content'))

        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='like', url_name='like')
    def like(self, request, pk):
        like, created = Like.objects.get_or_create(user=request.user, product=self.get_object())

        if not created:
           like.active = not like.active
           like.save()

        return Response(serializers.ProductDetailSerializer(self.get_object(), context={'request':request}).data,status= status.HTTP_200_OK)
    @action(methods=['post'], detail= True, url_path='rating', url_name='rating')
    def rating(self, request, pk):
        product = self.get_object()
        rating = request.data.get('rating')
        if not rating:
            return Response({'error': 'rating is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not 1 <= rating <= 5:
            return Response({'error': 'rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)

        product.rating = rating
        product.save()
        return Response(serializers.ProductDetailSerializer(product, context={'request': request}).data, status=status.HTTP_200_OK)
    @action(detail=True, methods=['get'], url_path='comments', url_name='comments')
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.all()
        return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)
    @action(detail=True, methods=['get'], url_path='likes', url_name='likes')
    def get_liked(self, request, pk):
        likes = self.get_object().like_set.filter(active=True).all()
        return Response(serializers.LikeSerializer(likes, many=True).data, status=status.HTTP_200_OK)

class ProductSearchView(viewsets.ViewSet,generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.query_params.get('name', None)
        price = self.request.query_params.get('price', None)
        shop = self.request.query_params.get('shop', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if price:
            queryset = queryset.filter(price__lte=price)
        if shop:
            queryset = queryset.filter(shop__shop_name__icontains=shop)

        return queryset[:20]  # Limit to 20 products
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

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def verify_user(self, request, pk=None):
        user = self.get_object()
        user.is_verified = True
        user.save()
        return Response({'status': 'user verified'}, status=status.HTTP_200_OK)


class UserRegistrationView(viewsets.ViewSet,generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser]



class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.OwnerAuthenticated]


class OrderCreateView(viewsets.ViewSet,generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Chức năng của Seller






# class RevenueStatisticsView(viewsets.ViewSet,generics.GenericAPIView):
#     permission_classes = [IsSeller]
#
#     @action(detail=True, methods=['get'])
#     def get(self, request, *args, **kwargs):
#         shop = request.user.shop
#         period = request.query_params.get('period', 'month')
#         now = datetime.now()
#
#         if period == 'month':
#             start_date = now.replace(day=1)
#         elif period == 'quarter':
#             start_date = now.replace(month=(now.month - 1) // 3 * 3 + 1, day=1)
#         elif period == 'year':
#             start_date = now.replace(month=1, day=1)
#         else:
#             return Response({'error': 'Invalid period'}, status=status.HTTP_400_BAD_REQUEST)
#
#         revenue = shop.product_set.filter(order__created_date__gte=start_date).aggregate(total_revenue=Sum('order__total_price'))
#         return Response(revenue, status=status.HTTP_200_OK)
#
#
#
# class BestSellingProductsView(viewsets.ViewSet,generics.GenericAPIView):
#     permission_classes = [IsSeller]
#     @action(detail=True, methods=['get'])
#     def get(self, request, *args, **kwargs):
#         shop = request.user.shop
#         best_selling_products = shop.product_set.annotate(sales_count=Count('order')).order_by('-sales_count')[:10]
#         return Response(serializers.ProductSerializer(best_selling_products, many=True).data, status=status.HTTP_200_OK)








