from django.db import models
from django.conf import settings
from django.utils import timezone

# 식품, 유통, 화학/건설/제조, 관광/금융/서비스
class Type(models.Model):
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

# 각 계열에 해당하는 회사 목록 
class Company(models.Model):
    company_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='types', null=True)
    subject = models.CharField('회사명', max_length=30, null=True)

    def __str__(self):
        return self.subject


####### post/models.py 합치기 #######

class Post(models.Model):
    boards_number = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='board', null=True)
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="author_user" )
    title = models.CharField('제목', max_length=100)
    desc = models.TextField('내용')

    scrap  = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="scrap_user")
    create_at = models.DateTimeField('작성시간', default = timezone.now)
    image = models.ImageField('사진', upload_to='images/', blank=True, null=True, name='image')

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="comment_user" )
    company_type = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    desc = models.CharField('내용', max_length=500)
    create_at = models.DateTimeField('작성시간', default = timezone.now)
    
    def __str__(self):
        return self.desc
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)