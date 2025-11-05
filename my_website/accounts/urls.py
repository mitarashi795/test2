# accounts/urls.py (この内容で全体を置き換えてください)
from django.urls import path
from . import views

urlpatterns = [
    # ログイン関連
    path('login/', views.RequestLoginCodeView.as_view(), name='request_login_code'),
    path('verify/', views.VerifyLoginCodeView.as_view(), name='verify_login_code'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/update/', views.profile_update_view, name='profile_update'), # プロフィール更新

    # 既存ページ (ログイン保護ビューへのリンク)
    path('', views.LandingPageView.as_view(), name='landing'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('accounts/', views.account_list_view, name='account_list'),
]