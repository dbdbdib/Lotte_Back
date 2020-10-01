from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField('제목', max_length=100)
    desc = models.TextField('내용')
    create_at = models.DateTimeField('작성시간', default = timezone.now)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null = True)
    desc = models.CharField('내용', max_length=500)
    create_at = models.DateTimeField('작성시간', default = timezone.now)
    
    def __str__(self):
        return self.desc
