

from django.urls import path, include
from rest_framework import routers
from shops import views


router = routers.DefaultRouter()
router.register('categories',views.CategoryViewSet, basename='categories')
router.register('shops',views.ShopViewSet, basename='shops')
router.register('products',views.ProductViewSet, basename='products')
router.register('users',views.UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),



]
