from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('board/<int:pk>', company, name='company')
]
