from django.contrib import admin
from .models import Type, Post, Company

# Register your models here.
admin.site.register(Type)
admin.site.register(Company)
admin.site.register(Post)