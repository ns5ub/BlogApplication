from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic
from .models import SimpleBlogPost, SimpleComment
from .forms import SimpleCommentForm
from django.shortcuts import render, get_object_or_404


class SimpleBlogPostList(generic.ListView):
    queryset = SimpleBlogPost.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class SimpleBlogPostDetail(generic.DetailView):
    model = SimpleBlogPost
    template_name = 'post_detail.html'


def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(SimpleBlogPost, slug=slug)
    comments = post.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        # comment has been added
        comment_form = SimpleCommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = SimpleComment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    reply_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    reply_comment.parent = parent_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.post = post
            # save
            new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = SimpleCommentForm()
    return render(request,
                  template_name,
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})
