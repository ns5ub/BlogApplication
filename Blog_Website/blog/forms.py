from .models import SimpleComment
from django import forms

class SimpleCommentForm(forms.ModelForm):
    # Default form for a simple comment
    class Meta:
        model = SimpleComment
        fields = ('name', 'email', 'body')