from django.forms import ModelForm

from .models import Post, Comment

from django import forms


class PostForms(ModelForm):
    class Meta:
        model = Post

        fields = ('boards', 'title', "desc", 'image')

        widget = {
            'title': forms.TextInput(attrs={'class': 'temp'}),
            'boards': forms.HiddenInput()
        }


class CommentForms(ModelForm):
    class Meta:
        model = Comment
        fields = ("desc",)