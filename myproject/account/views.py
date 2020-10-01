from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .forms import SignUpForm

# Create your views here.

# 회원가입 뷰
class SignUpView(CreateView): # 회원가입 기본 뷰 상속
    template_name = 'signup.html'
    form_class = SignUpForm # 폼은 SignUpForm 사용
    success_url = reverse_lazy('success_signup') # reverse_laze : 해당 url로 실행



# 회원가입 성공 뷰
class SuccessSignUpView(TemplateView):
    template_name = 'success_signup.html'
