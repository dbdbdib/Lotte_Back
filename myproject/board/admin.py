from django.contrib import admin
from .models import CompanyType, Company, Board

# Register your models here.
admin.site.register([CompanyType, Company, Board])