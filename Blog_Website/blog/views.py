from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import SimpleBlogPost


class SimpleBlogPostList(generic.ListView):
    queryset = SimpleBlogPost.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class SimpleBlogPostDetail(generic.DetailView):
    model = SimpleBlogPost
    template_name = 'post_detail.html'