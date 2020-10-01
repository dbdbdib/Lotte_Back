from django.forms import ModelForm

from .models import Post,Comment

class PostForms(ModelForm):
    class Meta:
        model = Post

        fields = ('title',"desc", 'image')
    
class CommentForms(ModelForm):
    class Meta:
        model = Comment
        fields = ("desc",)