from django.db import models
from django.contrib.auth.models import User

# Status: Is the post ready to publish?
STATUS = (
    (0, "Hidden"),
    (1, "Visible")
)


class SimpleBlogPost(models.Model):
    # SimpleBlogPost: Model for an actual blog post as stored in the database.
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)  # Slug: URL for the post
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # Assigning each blog post an author - default superuser in Django, but can be attached to an authentication service.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # On default, posts are visible, but can be hidden by changing this marker
    status = models.IntegerField(choices=STATUS, default=1)

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        # absolute URL of the post - post_detail is in urls.py so the reference can be modified in one place only
        from django.urls import reverse
        return reverse('post_detail', args=[str(self.slug)])

    def __str__(self):
        return self.title


class SimpleComment(models.Model):
    # Simple Comment: Allows for replies to the parent only for simplicity, but not multithreaded.
    # Associated with one single post: When the post is deleted, so are its comments
    post = models.ForeignKey(SimpleBlogPost, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=200, blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # On default, comments are visible, but can be hidden by changing this marker
    status = models.IntegerField(choices=STATUS, default=1)
    # A comment can have a parent, but it isn't required. A comment reply is a comment on a comment
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        # sort comments in chronological order by default
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment by {}'.format(self.name)
