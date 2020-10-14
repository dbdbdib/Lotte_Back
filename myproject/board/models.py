from django.db import models
from django.conf import settings

# 식품, 유통, 화학/건설/제조, 관광/금융/서비스
class Type(models.Model):
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

# 각 계열에 해당하는 회사 목록 
class Company(models.Model):
    company = models.ForeignKey(Type, related_name='companies', on_delete=models.CASCADE, null=True)
    subject = models.CharField('회사명', max_length=30, null=True)


# 각 회사 게시판에 글 쓰기
class Board(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, default='', null=True)
    name = models.CharField(max_length=30, null=True)