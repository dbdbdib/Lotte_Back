from django.contrib import admin
from .models import Food, Chem, Retail, Tour

# Register your models here.
admin.site.register(Food)
admin.site.register(Chem)
admin.site.register(Retail)
admin.site.register(Tour)