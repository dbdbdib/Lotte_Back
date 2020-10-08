from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# 일반 회원가입 폼
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

    class Meta:
        model = User # 모델은 User 사용
        fields = ['email', 'password1', 'password2', 'nickname', 'picture'] # 필드 지정

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        nickname = self.cleaned_data.get('nickname')

        # 이메일 확인 - 이 부분 끌어서 중복확인 기능 만들 것
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("이미 존재하는 이메일입니다.") # 존재하는 경우
        except User.DoesNotExist:
            pass
        if email is None: # email이 . 이 없는 경우 등 잘못 입력됐을 경우 None이 됨
            raise forms.ValidationError("올바른 이메일을 입력해주세요.")

        # 비밀번호 확인
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError:
            raise forms.ValidationError("8자 이하의 안전한 비밀번호로 설정해주세요.")
        if password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")


        # 닉네임 확인 - 이 부분 끌어서 중복확인 기능 만들 것
        if len(self.cleaned_data.get('nickname')) >= 20:
            raise forms.ValidationError('닉네임이 20자 이상입니다. 20자 미만으로 입력하세요.')
        try:
            User.objects.get(nickname=nickname)
            raise forms.ValidationError("이미 존재하는 닉네임입니다.")
        except User.DoesNotExist:
            pass

        return self.cleaned_data

    # 저장 메소드
    def save(self, commit=True, *args, **kwargs):
        user = super(SignUpForm, self).save(commit=False) # 본인의 부모(UserCreationForm)를 호출하여 저장 + 일단 보류
        
        # 추가 필드 저장
        user.email = self.cleaned_data['email']
        user.nickname = self.cleaned_data['nickname']
        user.picture = self.cleaned_data['picture']
        user.division = 0
        user.is_active = False

        if commit:
            user.save() # User 생성
        return user




# 현직자 회원가입 폼
class IncumbentSignUpForm(SignUpForm): # 일반 회원가입 폼 상속        
    # 필드
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        

        self.fields['line'].widget.attrs.update(
            {'placeholder': '계열 선택',
            'class':'pf_item',
             'id': "pf_gender",})

    class Meta:
        model = User # 모델은 User 사용
        fields = ['email', 'password1', 'password2', 'nickname', 'picture', 'line'] # 필드 지정
    
    # 에러메시지 처리하기
    def clean(self, *args, **kwargs):
        super(IncumbentSignUpForm, self).clean(*args, **kwargs)

        email = self.cleaned_data.get('email')
        line = self.cleaned_data.get('line')

        if email.split('@')[1] != 'naver.com': # 이메일의 @ 뒷부분 (추후 변경)
            raise forms.ValidationError('롯데 이메일 계정이 아닙니다.') # forms.ValidationError 보내면, views의 form_invalid()에서 form.non_field_errors()로
        if line is None:
            raise forms.ValidationError('계열을 입력하세요.') # forms.ValidationError 보내면, views의 form_invalid()에서 form.non_field_errors()로


        return self.cleaned_data
    
    # 저장 메소드
    def save(self, commit=True, *args, **kwargs):
        user = super(IncumbentSignUpForm, self).save(commit=False, *args, **kwargs) # 본인의 부모(UserCreationForm)를 호출하여 저장 + 일단 보류
        
        # 추가 필드 저장
        user.division = 1
        user.line = self.cleaned_data['line']
        user.is_active = False

        if commit:
            user.save() # User 생성
        return user




# 로그인 폼
class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)        

        # 아이디 대신 이메일을 username으로
        UserModel = User



class UserUpdateForm(forms.ModelForm):

    # nickname = forms.CharField(
    #     label='닉네임',
    #     widget=forms.TextInput(attrs={}),
    #     required=True,
    # )

    # picture = forms.ImageField(
    #     label='프로필 사진',
    #     widget=forms.TextInput(attrs={}),
    #     required=False,
    # )


    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['nickname'].widget.attrs.update(
            {'placeholder': '닉네임',
             'class': "pf_item",
             'id': "pf_phone"})

        self.fields['picture'].widget.attrs.update(
            {'placeholder': '프로필 사진',
            'class':'pf_item',
             'id': "pf_gender",})

    class Meta:
        model = User
        fields = ['nickname', 'picture',]

class PasswordUpdateForm(PasswordChangeForm):
    # 필드
    old_password = forms.CharField(
        label='기존 비밀번호',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
        required=False
    )
    new_password1 = forms.CharField(
        label='새 비밀번호',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    new_password2 = forms.CharField(
        label='새 비밀번호 확인',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False
    )

    # # 에러메시지
    # error_messages = {
    #     'password_mismatch': '비밀번호가 다릅니다.',
    # }
