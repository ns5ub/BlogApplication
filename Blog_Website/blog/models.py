from django.db import models
from django.contrib.auth.models import User

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class SimpleBlogPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', args=[str(self.slug)])
        #return ('post_detail', (), {'slug': self.slug})

    def __str__(self):
        return self.title


class SimpleComment(models.Model):
    post = models.ForeignKey(SimpleBlogPost, related_name='comments', on_delete= models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=200, blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.DO_NOTHING)

    class Meta:
        # sort comments in chronological order by default
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment by {}'.format(self.name)


