from .models import SimpleComment
from django import forms


class SimpleCommentForm(forms.ModelForm):
    class Meta:
        model = SimpleComment
        fields = ('name', 'email', 'body')