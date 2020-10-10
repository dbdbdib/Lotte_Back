from django.db import models

# Create your models here.
class Food(models.Model):
    # 회사명
    workplace = models.CharField(max_length=20)

    def __str__(self):
        return self.workplace

class Chem(models.Model):
    workplace = models.CharField(max_length=20)

    def __str__(self):
        return self.workplace

class Retail(models.Model):
    workplace = models.CharField(max_length=20)

    def __str__(self):
        return self.workplace

class Tour(models.Model):
    workplace = models.CharField(max_length=20)

    def __str__(self):
        return self.workplace