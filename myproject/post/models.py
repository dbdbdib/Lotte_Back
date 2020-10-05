
# Create your models here.
from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Post(models.Model):
    # author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name="author_user" )
    title = models.CharField('제목', max_length=100)
    desc = models.TextField('내용')
    # scrap  = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="scrap_user")
    create_at = models.DateTimeField('작성시간', default = timezone.now)
    image = models.ImageField('사진',upload_to='images/', blank=True, null=True, name='image')
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null = True)
    desc = models.CharField('내용', max_length=500)
    create_at = models.DateTimeField('작성시간', default = timezone.now)
    
    def __str__(self):
        return self.desc


# class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)