

from django.urls import path, include
from rest_framework import routers
from shops import views


router = routers.DefaultRouter()
router.register('categories',views.CategoryViewSet, basename='categories')
router.register('shops',views.ShopViewSet, basename='shops')


urlpatterns = [
    path('', include(router.urls)),



]
