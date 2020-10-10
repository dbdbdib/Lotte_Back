from django.db import models
# 대분류


class CompanyType(models.Model):
    company_type = models.CharField(max_length=20)

    def __str__(self):
        return self.company_type

    class Meta:
        verbose_name = '4계열' # 단수
        verbose_name_plural = '4계열' # 복수


    
# 계열사


class Company(models.Model):
    company_type = models.ForeignKey(
        CompanyType, on_delete=models.CASCADE)  # onetoMany = foreignkey
    company_name = models.CharField('회사명', max_length=30, null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = '계열사' # 단수
        verbose_name_plural = '계열사' # 복수



# 게시판


class Board(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '계열사별 계시판' # 단수
        verbose_name_plural = '계시판' # 복수

