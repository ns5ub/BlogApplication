from django.contrib import admin

# Register your models here.
from .models import SimpleBlogPost, SimpleComment


@admin.register(SimpleBlogPost)
class SimpleBlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SimpleComment)
class SimpleCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'status')
    list_filter = ('status', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['delete_comments']

    def delete_comments(self, request, queryset):
        queryset.update(active=False)

