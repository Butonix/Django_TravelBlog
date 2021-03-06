from django import forms
from ckeditor.widgets import CKEditorWidget
from . import models

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'text', 'tags', 'author', 'slug']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['detail', ]

