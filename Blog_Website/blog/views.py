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

    # Get the comments in order by reply
    comments_ordered = get_nested_comments(post)
    count = len(comments_ordered)

    # If a comment has been added: do the following
    if request.method == 'POST':
        # Get the form
        comment_form = SimpleCommentForm(data=request.POST)
        if comment_form.is_valid():
            # Get the parent id:
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None

            # Get the parent comment
            parent_obj = None
            if parent_id:
                parent_obj = SimpleComment.objects.get(id=parent_id)
                if parent_obj:
                    # create reply comment object
                    reply_comment = comment_form.save(commit=False)
                    reply_comment.parent = parent_obj

            # Else, it is a normal comment
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
                   'comment_form': comment_form,
                   'comments_ordered': comments_ordered,
                   'count' : count,
                   })


# Function to get the comments in order given a post
def get_nested_comments(post):
    # Get the comments without a parent, pass to the recursive function
    parent_comments = post.comments.filter(status=1, parent__isnull=True).order_by('-created_on')
    comments_ordered = []
    comments_ordered= get_nested_comments_helper(parent_comments, comments_ordered, indent=0)
    return comments_ordered


def get_nested_comments_helper(comment_list, comments_ordered, indent = 0):
    for c in comment_list:
        # For each comment, add it to the list. Then call the same function on it's list of replies
        comments_ordered.append((c,indent, 12-indent))
        c_replies = c.replies.all()
        if c_replies:
            # Pass in and edit the same list to build it up. Increment the indent for each level.
            comments_ordered = get_nested_comments_helper(c_replies, comments_ordered, indent=indent + 1)
    return comments_ordered
