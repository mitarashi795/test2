# accounts/urls.py (この内容で全体を置き換えてください)
from django.urls import path
from . import views

urlpatterns = [
    # ログイン関連
    path('ajax/login/', views.custom_login, name='ajax_login'),
    path('logout/', views.custom_logout, name='logout'),

    # ページ表示関連
    path('', views.LandingPageView.as_view(), name='landing'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('accounts/', views.AccountListView.as_view(), name='account_list'),
    path('switch_account/<int:pk>/', views.switch_account, name='switch_account'),

    # 承認関連
    path('wait_for_approval/', views.WaitForApprovalView.as_view(), name='wait_for_approval'),
    path('approval/', views.ApprovalListView.as_view(), name='approval_list'),
    path('approve/<int:pk>/', views.approve_request, name='approve_request'),
]