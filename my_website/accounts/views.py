# accounts/views.py (この内容で全体を置き換えてください)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views import View
import json

from .models import LoginRequest


# --- ログアウト処理 ---
def custom_logout(request):
    # セッションからアカウント関連の情報をすべて削除
    for key in list(request.session.keys()):
        if not key.startswith('_'): # Django内部キー以外
             del request.session[key]
    return redirect('landing') # ログアウト後はトップページ

# --- アカウント一覧ページ ---
class AccountListView(View):
    def get(self, request, *args, **kwargs):
        my_account_ids = request.session.get('my_account_ids', [])
        if not my_account_ids:
             if not request.session.get('login_request_id'):
                 return redirect('landing')
             my_account_ids = [request.session.get('login_request_id')]

        my_accounts = LoginRequest.objects.filter(id__in=my_account_ids).order_by('-timestamp')
        context = {
            'my_accounts': my_accounts,
        }
        return render(request, 'accounts/account_list.html', context)

# --- アカウント切り替え処理 ---
def switch_account(request, pk):
    my_account_ids = request.session.get('my_account_ids', [])
    login_request_id = request.session.get('login_request_id')

    if not login_request_id:
        return redirect('landing')

    if pk in my_account_ids:
        account_to_switch = get_object_or_404(LoginRequest, pk=pk)
        request.session['login_request_id'] = account_to_switch.id
        request.session['user_role'] = account_to_switch.role

        if account_to_switch.is_approved:
            return redirect('dashboard')
        else:
            return redirect('wait_for_approval')

    return redirect('account_list')

# --- 承認待ちページ ---
class WaitForApprovalView(View):
    def get(self, request, *args, **kwargs):
        login_request_id = request.session.get('login_request_id')
        if not login_request_id: return redirect('landing')
        login_request = get_object_or_404(LoginRequest, id=login_request_id)
        if login_request.is_approved: return redirect('dashboard')
        return render(request, 'accounts/wait_for_approval.html', {'login_request': login_request})

# --- 承認リストページ ---
class ApprovalListView(View):
    def get(self, request, *args, **kwargs):
        login_request_id = request.session.get('login_request_id')
        if not login_request_id: return redirect('landing')

        current_user = get_object_or_404(LoginRequest, id=login_request_id)
        if current_user.role not in ['教員', '実行委員長']:
            return HttpResponseForbidden("アクセス権限がありません。")

        pending_requests = []
        if current_user.role == '教員':
            pending_requests = LoginRequest.objects.filter(role='実行委員長', is_approved=False).order_by('timestamp')
        elif current_user.role == '実行委員長':
            pending_requests = LoginRequest.objects.filter(role='委員長', is_approved=False).order_by('timestamp')

        context = {'current_user': current_user, 'pending_requests': pending_requests}
        return render(request, 'accounts/approval_list.html', context)

# --- 承認アクション ---
def approve_request(request, pk):
    approver_id = request.session.get('login_request_id')
    if not approver_id: return redirect('landing')

    approver = get_object_or_404(LoginRequest, id=approver_id)
    request_to_approve = get_object_or_404(LoginRequest, pk=pk)

    can_approve = False
    if approver.role == '教員' and request_to_approve.role == '実行委員長':
        can_approve = True
    elif approver.role == '実行委員長' and request_to_approve.role == '委員長':
        can_approve = True

    if not can_approve:
        return HttpResponseForbidden("承認権限がありません。")

    if request.method == 'POST':
        request_to_approve.is_approved = True
        request_to_approve.save()
    
    return redirect('approval_list')

# --- トップページ（ランディングページ） ---
class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        # ★★★ ここを 'accounts/landing.html' に修正 ★★★
        return render(request, 'accounts/landing.html')

# --- ダッシュボード ---
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        login_request_id = request.session.get('login_request_id')
        if not login_request_id: return redirect('landing')

        login_request = get_object_or_404(LoginRequest, id=login_request_id)
        if not login_request.is_approved and login_request.role in ['実行委員長', '委員長']:
            return redirect('wait_for_approval')

        # ★★★ ここも 'accounts/dashboard.html' に修正 ★★★
        return render(request, 'accounts/dashboard.html', {'login_request': login_request})