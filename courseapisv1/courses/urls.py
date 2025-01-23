from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses import views

r = DefaultRouter()
r.register('categories', views.CategoryViewSet, basename='category')
r.register('courses', views.CourseViewSet, basename='course')
r.register('lessons', views.LessonViewSet, basename='lesson')
r.register('users', views.UserViewSet, basename='user')
r.register('comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(r.urls))
]
