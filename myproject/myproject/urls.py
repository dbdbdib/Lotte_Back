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
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from account.views import SelectDivisionView, SignUpView, IncumbentSignUpView, SuccessSignUpView, ActivateView, SignInView, MypageView, UpdateMypageView
from board.views import MainPageView, food, food_board, chem, retail, tour
from post.views import index, detail
# for Media file전달
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='mainpage'),
    path('select_division', SelectDivisionView.as_view(), name='select_division'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('incumbent_signup/', IncumbentSignUpView.as_view(), name='incumbent_signup'),
    path('success_signup/', SuccessSignUpView.as_view(), name='success_signup'),
    path('account/activate/<str:uidb64>/<str:token>', ActivateView.as_view(), name='activate'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mypage/<int:pk>/', MypageView.as_view(), name='mypage'),
    path('mypage/<int:pk>/update', UpdateMypageView.as_view(), name='update_mypage'),
    # path('mypage/<int:pk>/update/nickname_update', NicknameUpdate(), name='nickname_update')
    path('food/', food, name='food'),
    path('retail/', retail, name='retail'),
    path('chem/', chem, name='chem'),
    path('tour/', tour, name='tour'),

    path('food/post/<int:board_id>', index, name="food_post"),
    path('retail/post/<int:board_id>', index, name="retail_post"),
    path('chem/post/<int:board_id>', index, name="chem_post"),
    path('tour/post/<int:board_id>', index, name="tour_post"),

    path('', include('post.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
