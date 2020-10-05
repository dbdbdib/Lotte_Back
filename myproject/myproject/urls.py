"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from account.views import SignUpView, IncumbentSignUpView, ActivateView, SignInView, MainPageView, MyPageView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='mainpage'), # name 넣는 것 필수 (안 하면 오류나더라)
    path('signup/', SignUpView.as_view(), name='signup'),
    path('incumbent_signup/', IncumbentSignUpView.as_view(), name='incumbent_signup'),
    path('account/activate/<str:uidb64>/<str:token>', ActivateView.as_view(), name='activate'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mypage/<int:pk>/', MyPageView.as_view(), name='mypage'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # 이미지 올릴 때 필요
=======
from django.urls import path, include
from account.views import SignUpView, SuccessSignUpView
from board.views import main, food, chem, retail, tour

# for Media file전달
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view(), name='signup'), # name 넣는 것 필수 (안 하면 오류나더라)
    path('success_signup/', SuccessSignUpView.as_view(), name='success_signup'),
    path('', main, name='main'),
    path('food/', food, name='food'),
    path('retail/', retail, name='retail'),
    path('chem/', chem, name='chem'),
    path('tour/', tour, name='tour'),
    path('', include('post.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 464f568c4fa98a654d48de8e4e8bdea8c3f6c465
