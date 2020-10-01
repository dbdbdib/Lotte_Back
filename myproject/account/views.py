from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import resolve_url
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.contrib import messages
from .forms import SignUpForm, SignInForm

# Create your views here.

# 회원가입 뷰
class SignUpView(CreateView): # 회원가입 기본 뷰 상속
    template_name = 'registration/signup.html'
    form_class = SignUpForm # 폼은 SignUpForm 사용

    def get_success_url(self):
        return reverse_lazy('success_signup') # reverse_laze : 해당 url로 실행


# 회원가입 성공 뷰
class SuccessSignUpView(TemplateView):
    template_name = 'registration/success_signup.html'


# 로그인 뷰
class SignInView(LoginView):
    template_name = 'registration/signin.html'
    form_class = SignInForm # 폼은 SignInForm 사용
    authentication_form = SignInForm

    def get_success_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL) # 로그인 후, LOGIN_REDIRECT_URL로 넘어가기 (mainpage)

    def form_invalid(self, form_class):
        messages.error(self.request, '로그인에 실패하였습니다. ID 또는 Password를 확인해 주세요.', extra_tags='danger')
        return super().form_invalid(form_class)


# 메인페이지 뷰
class MainPageView(TemplateView):
    template_name = 'mainpage.html'