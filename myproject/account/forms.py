from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

# 회원가입 폼
class SignUpForm(UserCreationForm): # 회원가입 기본 폼 상속 (패스워드, 패스워드확인)        
    # 필드
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)        

        self.fields['email'].widget.attrs.update(
            {'placeholder': '이메일',
            'class': "pf_item",
             'id': "pf_name"})

        self.fields['password1'].label = '비밀번호' # 라벨 수정
        self.fields['password1'].widget.attrs.update(
            {'label-name': '비밀번호',
            'placeholder': '비밀번호',
            'class': "pf_item",
             'id': "pf_nickname"})

        self.fields['password2'].label = '비밀번호 확인' # 라벨 수정
        self.fields['password2'].widget.attrs.update(
            {'placeholder': '비밀번호 확인',
            'class':'pf_item',
             'id': "pf_birth"})
        self.fields['password2'].help_text = "" # 부모 UserCreationForm의 help_text 출력 X

        self.fields['nickname'].widget.attrs.update(
            {'placeholder': '닉네임',
             'class': "pf_item",
             'id': "pf_phone"})

        self.fields['picture'].widget.attrs.update(
            {'placeholder': '프로필 사진',
            'class':'pf_item',
             'id': "pf_gender",})

        # 가입 구분 선택
        DIVISION_CHOICES = (
            (0, '취준생'),
            (1, '현직자'),
        )

        self.fields['division'].widget = forms.RadioSelect(choices = DIVISION_CHOICES) # 라디오 버튼으로
        self.fields['division'].widget.attrs.update(
            {'placeholder': '가입 구분',
            'class':'pf_item',
             'id': "pf_email"})

        self.fields['line'].widget.attrs.update(
            {'placeholder': '계열',
            'class':'pf_item',
             'id': "pf_email"})

    # 부모 UserCreationForm의 에러 메시지 수정
    error_messages = {
        'password_mismatch': "비밀번호가 일치하지 않습니다.",
    }

    class Meta:
        model = User # 모델은 User 사용
        fields = ['email', 'password1', 'password2', 'nickname', 'picture', 'division', 'line'] # 필드 지정
    
    # 저장 메소드
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False) # 본인의 부모(UserCreationForm)를 호출하여 저장 + 일단 보류
        
        # 추가 필드 저장
        user.email = self.cleaned_data['email']
        user.nickname = self.cleaned_data['nickname']
        user.picture = self.cleaned_data['picture']
        user.division = self.cleaned_data['division']
        user.line = self.cleaned_data['line']

        if commit:
            user.save() # User 생성
        return user


# 로그인 폼
class SignInForm(AuthenticationForm):
    # AuthenticationForm의 에러메시지 수정
    error_messages = {
        'invalid_login': '아이디 또는 비밀번호가 틀렸습니다.',
        'inactive': "This account is inactive.",
    }

    # 필드
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)        

        # 아이디 대신 이메일을 username으로
        UserModel = User