from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

# django 모델들은 Manager를 통해서 QuerySet을 받기 때문에, DB에서 query를 처리할 때 Manager를 거쳐야 함
# 따라서, User를 Custom할거니 UserManager도 함께 커스텀
class UserManager(BaseUserManager): # BaseUserManager : User 생성 시 모델 관리 및 생성 시 기능 지정
    
    # user 생성 메소드 - 이메일, 패스워드, 닉네임 기본 ++ 사진, 계열은 superuser에서 필수 아니므로 초기화 
    def _create_user(self, email, password, nickname, picture = None, line = 0, **extra_fields):
        if not email: # 이메일 필수
            raise ValueError('The given email must be set')

        user = self.model(
            email=self.normalize_email(email), # 이메일 정규화
            nickname=nickname,
            picture=picture,
            line=line,
            **extra_fields
        )

        user.set_password(password) # 비밀번호 설정
        user.save(using=self._db) # 저장
        return user

    # user 중 일반user 생성 메소드
    def create_user(self, email, nickname, password, **extra_fields):
        extra_fields.setdefault('is_staff', False) # 스태프 X
        extra_fields.setdefault('is_superuser', False) # 슈퍼유저 X

        return self._create_user(email, password, nickname, **extra_fields) # user 생성

    # user 중 superuser 생성 메소드 - 이메일, 패스워드, 닉네임은 필수
    def create_superuser(self, email, password, nickname, **extra_fields):
        extra_fields.setdefault('is_staff', True) # 스태프 O
        extra_fields.setdefault('is_superuser', True) # 슈퍼유저 O

        # 에러 잡기
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self._create_user(email, password, nickname, **extra_fields) # user 생성



# AbstractBaseUser : 이것을 상속받아 모델을 재구성 (AbstractUser는 기본 필드 모델을 새로 정의할 수 없기 때문에 사용 X)
# PermissionsMixin : 권한 관련(is_staff 등) 모여있는 클래스 - 상속받아 모델 재구성
class User(AbstractBaseUser, PermissionsMixin):
    # 취준생 or 현직자 구분 선택
    DIVISION_CHOICES = (
        (0, '취준생'),
        (1, '현직자'),
    )
    
    # 현직자일 경우 계열 선택
    LINE_CHOICES = (
        (0, '식품'),
        (1, '유통'),
        (2, '화학/건설/제조'),
        (3, '관광/서비스/금융')
    )
    
    # 필드 정의
    email = models.EmailField('이메일', unique=True)
    nickname = models.CharField('닉네임', max_length=20)
    picture = models.ImageField('프로필 사진', null=True, default="./static/img/userdefaultimg.png")
    division = models.IntegerField('가입 구분', choices = DIVISION_CHOICES)
    line = models.IntegerField('계열', choices = LINE_CHOICES, null=True)
    is_staff = models.BooleanField('staff',default=False) # is_staff는 넣어야 함 (is_superuser는 이미 있어서 O)

    objects = UserManager() # Manager 지정
    USERNAME_FIELD = 'email' # username을 일반 ID 대신, email 그 자체로
    REQUIRED_FIELDS = ['nickname'] # 필수 필드(email, password는 기본 지정o)

    class Meta:
        verbose_name = '사용자' # 단수
        verbose_name_plural = '사용자들' # 복수

    def __str__(self):
        return self.email