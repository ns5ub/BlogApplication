from . import views
from django.urls import path

urlpatterns = [
    path('', views.SimpleBlogPostList.as_view(), name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    #path('<slug:slug>/', views.SimpleBlogPostDetail.as_view(), name='post_detail'),
]