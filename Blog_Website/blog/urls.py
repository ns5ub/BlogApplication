from . import views
from django.urls import path

urlpatterns = [
    path('', views.SimpleBlogPostList.as_view(), name='home'),
    path('<slug:slug>/', views.SimpleBlogPostDetail.as_view(), name='post_detail'),
]