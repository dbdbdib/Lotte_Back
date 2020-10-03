from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import resolve_url
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .token import account_activation_token
from .text import message
from .forms import SignUpForm, IncumbentSignUpForm, SignInForm
from .models import User

# Create your views here.

# 회원가입 뷰
class SignUpView(CreateView): # 회원가입 기본 뷰 상속
    template_name = 'registration/signup.html'
    form_class = SignUpForm # 폼은 SignUpForm 사용

    def get_success_url(self):
        return reverse_lazy('mainpage') # reverse_laze : 해당 url로 실행

    def form_valid(self, form):
        user = form.save() # 폼 저장할 때 return한 user 가져와서 저장
        auth.login(self.request, user) # 자동 로그인
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors(), extra_tags='danger')
        return super().form_invalid(form)



# 현직자 회원가입 뷰
class IncumbentSignUpView(CreateView):
    template_name = 'registration/incumbent_signup.html'
    form_class = IncumbentSignUpForm # 폼은 IncumbentSignUpForm 사용
    user = None

    def get_success_url(self):
        # 인증이메일 보내기
        domain = "http://127.0.0.1:8000/" # 추후 변경
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        message_data = message(domain, uidb64, token)

        email = EmailMessage(
            '이메일 인증을 완료해주세요.',
            message(domain, uidb64, token),
            to=[self.user.email]
        )
        email.send()

        return reverse_lazy('mainpage') # reverse_laze : 해당 url로 실행

    def form_valid(self, form):
        self.user = form.save() # 폼 저장할 때 return한 user 가져와서 저장
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors(), extra_tags='danger')
        return super().form_invalid(form)



# 이메일 인증 처리 뷰
class ActivateView(TemplateView):
    template_name = 'registration/activate.html'

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid) # user pk가 동일한지 확인

            if account_activation_token.check_token(user, token): # 동일하면
                user.is_active = True # active로 변경
                user.save() # 저장
                auth.login(request, user)

                return super(ActivateView, self).get(request, uidb64, token)

            return JsonResponse({"message": "AUTH FAIL"}, status=400) # 다르면 에러
        
        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        except KeyError:            
            return JsonResponse({"message": "INVALID_KEY"}, status=400)
    
    

# 로그인 뷰
class SignInView(LoginView):
    template_name = 'registration/signin.html'
    form_class = SignInForm # 폼은 SignInForm 사용
    authentication_form = SignInForm

    def get_success_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL) # 로그인 후, LOGIN_REDIRECT_URL로 넘어가기 (mainpage)

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다. ID 또는 Password를 확인해 주세요.', extra_tags='danger')
        return super().form_invalid(form)

# 메인페이지 뷰
class MainPageView(TemplateView):
    template_name = 'mainpage.html'
    
    # context 뿌리는 메소드
    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs) # pk, view 포함

        user = self.request.user
        context = {'user': user}
        return context



# 마이페이지 뷰
class MyPageView(TemplateView):
    template_name = 'mypage.html'
    pk_url_kwargs = 'pk' # path로부터 전달받을 pk 키워드 이름

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs) # pk, view 포함

        user = self.request.user
        pk = self.kwargs.get(self.pk_url_kwargs)

        context = {'user': user, 'pk': pk}
        return context