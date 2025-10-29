# accounts/urls.py (この内容で全体を置き換えてください)
from django.urls import path
from . import views

urlpatterns = [
    # ログイン関連
    # ★ 'RequestLoginCodeView' が存在しないため、古い 'custom_login' 関数を指します
    path('login/', views.custom_login, name='request_login_code'), 
    
    # ★ 存在しないビューをコメントアウト
    # path('verify/', views.VerifyLoginCodeView.as_view(), name='verify_login_code'),
    
    path('logout/', views.custom_logout, name='logout'),
    
    # ★ 存在しないビューをコメントアウト
    # path('profile/update/', views.profile_update_view, name='profile_update'), 

    # 既存ページ (ログイン保護ビューへのリンク)
    path('', views.LandingPageView.as_view(), name='landing'),
    
    # ★ 関数ではなく ClassView として呼び出すように修正
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('accounts/', views.AccountListView.as_view(), name='account_list'),
    
    # 承認関連
    # ★ 関数ではなく ClassView として呼び出すように修正
    path('wait_for_approval/', views.WaitForApprovalView.as_view(), name='wait_for_approval'),
    path('approval/', views.ApprovalListView.as_view(), name='approval_list'),
    
    path('approve/<int:pk>/', views.approve_request, name='approve_request'),

    # ★ 'account_list.html' テンプレートが使用する 'switch_account' へのURLが不足していたため追加
    path('switch/<int:pk>/', views.switch_account, name='switch_account'),
]
