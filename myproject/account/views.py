from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import resolve_url, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
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
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import SignUpForm, IncumbentSignUpForm, SignInForm, NicknameUpdateForm, PictureUpdateForm, PasswordUpdateForm
from .models import User

# Create your views here.

# 회원가입 구분 선택 뷰
class SelectDivisionView(TemplateView):
    template_name = 'registration/select_division.html'



# 회원가입 뷰
class SignUpView(CreateView): # 회원가입 기본 뷰 상속
    template_name = 'registration/signup.html'
    form_class = SignUpForm # 폼은 SignUpForm 사용
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

        return reverse_lazy('success_signup') # reverse_laze : 해당 url로 실행

    def form_valid(self, form):
        self.user = form.save() # 폼 저장할 때 return한 user 가져와서 저장해두기
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors(), extra_tags='danger')
        return super().form_invalid(form)



# 현직자 회원가입 뷰
class IncumbentSignUpView(SignUpView):
    template_name = 'registration/incumbent_signup.html'
    form_class = IncumbentSignUpForm # 폼은 IncumbentSignUpForm 사용



# 회원가입 입력 완료 뷰
class SuccessSignUpView(TemplateView):
    template_name = 'registration/success_signup.html'



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
                auth.login(request, user) # 자동 로그인

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



# 마이페이지 뷰
class MypageView(TemplateView):
    template_name = 'mypage/mypage.html'

    # context 뿌리는 메소드
    def get_context_data(self, **kwargs):

        user = self.request.user
        context = {'user': user}
        return context



# 마이페이지 정보 수정
class UpdateMypageView(TemplateView):
    ### TemplateResponseMixin
    template_name = 'mypage/update_mypage.html'

    ### ContextMixin 
    def get_context_data(self, **kwargs):
        """ Adds extra content to our template """
        context = super(UpdateMypageView, self).get_context_data(**kwargs)

        context['nickname_form'] = NicknameUpdateForm(
            instance = self.request.user,
            prefix='nickname_form', 
            data = self.request.POST if 'nickname_form-submit' in self.request.POST else None,
            )

        context['picture_form'] = PictureUpdateForm(
            instance = self.request.user,
            prefix='picture_form', 
            data = self.request.POST if 'picture_form-submit' in self.request.POST else None,
            files = self.request.FILES if 'picture_form-submit' in self.request.POST else None
            )

        context['password_form'] = PasswordUpdateForm(
            user = self.request.user,
            prefix='password_form', 
            # Multiple 'submit' button paths should be handled in form's .save()/clean()
            data = self.request.POST if 'password_form-submit' in self.request.POST else None,
            )

        return context


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if context['nickname_form'].is_valid():
            context['nickname_form'].save()
            messages.success(request, '닉네임 변경o')
        elif context['picture_form'].is_valid():
            context['picture_form'].save()
            messages.success(request, '사진 변경o')
        elif context['password_form'].is_valid():
            context['password_form'].save()
            update_session_auth_hash(request, self.request.user)  # 암호화하여 업뎃
            messages.success(request, '비번 변경o')
        else:
            messages.error(request, '저장x, 다시 확인')

        return self.render_to_response(context)