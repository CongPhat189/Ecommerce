from django.urls import path, include
from rest_framework import routers
from shops import views


router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('shops', views.ShopViewSet, basename='shops')
router.register('products', views.ProductViewSet, basename='products')
router.register('users', views.UserViewSet, basename='users')

router.register('comments', views.CommentViewSet, basename='comments')
router.register('register', views.UserRegistrationView, basename='register')

router.register('search-products', views.ProductSearchView, basename='products-search')
router.register('create-order', views.OrderCreateView, basename='create-order')
# router.register('register-shop', views.ShopRegistrationView, basename='register-shop')
# router.register('add-product', views.ProductCreateView, basename='add-product')
# router.register('revenue-statistics', views.RevenueStatisticsView, basename='revenue-statistics')
# router.register('best-selling-products', views.BestSellingProductsView, basename='best-selling-products')


urlpatterns = [
    path('', include(router.urls)),

]
