from django.views import generic
from .models import SimpleBlogPost, SimpleComment
from .forms import SimpleCommentForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

# Create your views here.


class SimpleBlogPostList(generic.ListView):
    # Using the given "List View" to list out all of the simple blog posts
    queryset = SimpleBlogPost.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class SimpleBlogPostDetail(generic.DetailView):
    # Original Post Detail for a Blog Post
    # path('<slug:slug>/', views.SimpleBlogPostDetail.as_view(), name='post_detail'),
    model = SimpleBlogPost
    template_name = 'post_detail.html'


def post_detail(request, slug):
    # Get the Post that corresponds to the slug, or URL
    template_name = 'post_detail.html'
    post = get_object_or_404(SimpleBlogPost, slug=slug)

    # Get the comments which do not have a parent themselves
    comments = post.comments.filter(active=True, parent__isnull=True)

    # If a comment has been added: do the dollowing
    if request.method == 'POST':
        # Get the form
        comment_form = SimpleCommentForm(data=request.POST)
        if comment_form.is_valid():
            # Get the parent id:
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None

            # Get the parent comment
            if parent_id:
                parent_obj = SimpleComment.objects.get(id=parent_id)
                if parent_obj:
                    # create reply comment object
                    reply_comment = comment_form.save(commit=False)
                    reply_comment.parent = parent_obj

            # Else, it is a normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())  # Redirect user to post
    else:
        # If not a post, just output the form
        comment_form = SimpleCommentForm()
    return render(request,
                  template_name,
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})
