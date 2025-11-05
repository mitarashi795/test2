# accounts/views.py (この内容で全体を置き換えてください)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views import View
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse_lazy
from datetime import timedelta
import secrets
import string
import json

# ★ フォームのインポートを更新
from .forms import EmailForm, VerifyCodeForm, ProfileUpdateForm
from .models import LoginRequest

def get_random_password_string(length):
    """
    指定された長さのランダムな英数字文字列を生成する
    (string.ascii_letters + string.digits)
    """
    pass_chars = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(pass_chars) for x in range(length))
    return password

# --- ログイン保護デコレータ ---
def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('login_request_id'):
            return redirect('request_login_code') # メールアドレス入力ページへ
        return view_func(request, *args, **kwargs)
    return wrapper

# --- メールアドレス入力 & コード送信 ---
class RequestLoginCodeView(View):
    def get(self, request, *args, **kwargs):
        if request.session.get('login_request_id'):
            return redirect('dashboard')
        form = EmailForm()
        return render(request, 'accounts/request_code.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if request.session.get('login_request_id'):
            return redirect('dashboard')
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # メールアドレスでユーザーを検索、なければ新規作成 (仮登録)
            # ★ 承認機能を削除したため、is_approved はデフォルトで True に設定
            login_request, created = LoginRequest.objects.get_or_create(
                email=email,
                defaults={
                    'name': email.split('@')[0], 
                    'role': '部活動関係者', # 仮の役職
                    'is_approved': True # ★ 常に承認済みに
                }
            )
            
            # ★ 既存ユーザーが未承認だった場合も、このタイミングで承認済みに更新
            if not login_request.is_approved:
                login_request.is_approved = True

            code = get_random_password_string(6)
            expiry_time = timezone.now() + timedelta(minutes=10) # 10分間有効

            login_request.otp_code_hash = make_password(code)
            login_request.otp_expiry = expiry_time
            login_request.save()

            # メール送信
            subject = '認証コードのお知らせ'
            message = f'認証コードは {code} です。10分以内にご入力ください。'
            from_email = 'noreply@yourdomain.com' # settings.pyのDEFAULT_FROM_EMAIL推奨
            recipient_list = [email]
            
            try:
                # settings.pyのEMAIL_BACKEND設定により、開発中はコンソールに出力されます
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as e:
                print(f"メール送信エラー: {e}") # ターミナルにログ出力
                form.add_error(None, 'メールの送信に失敗しました。時間をおいて再試行してください。')
                return render(request, 'accounts/request_code.html', {'form': form})

            request.session['login_email_pending'] = email
            return redirect('verify_login_code')

        return render(request, 'accounts/request_code.html', {'form': form})

# --- コード検証 & ログイン ---
class VerifyLoginCodeView(View):
    def get(self, request, *args, **kwargs):
        email = request.session.get('login_email_pending')
        if not email:
            return redirect('request_login_code')
        form = VerifyCodeForm()
        return render(request, 'accounts/verify_code.html', {'form': form, 'email': email})

    def post(self, request, *args, **kwargs):
        email = request.session.get('login_email_pending')
        if not email:
            return redirect('request_login_code')

        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                login_request = LoginRequest.objects.get(email=email)

                # コードと有効期限をチェック
                if (login_request.otp_code_hash and
                        check_password(code, login_request.otp_code_hash) and
                        login_request.otp_expiry and
                        login_request.otp_expiry > timezone.now()):

                    login_request.otp_code_hash = None
                    login_request.otp_expiry = None
                    login_request.is_approved = True # ★ 念のためここでも承認済みに
                    login_request.save()

                    # セッションにログイン情報を保存し、有効期限を1週間に設定
                    request.session['login_request_id'] = login_request.id
                    request.session['user_role'] = login_request.role
                    request.session.set_expiry(timedelta(weeks=1)) # 1週間

                    if 'login_email_pending' in request.session:
                        del request.session['login_email_pending']
                    
                    # 役職や氏名が未設定（仮登録のまま）なら、プロフィール更新ページへ
                    if login_request.name == email.split('@')[0]:
                         return redirect('profile_update')

                    # ★ 承認待ちのチェックを削除し、ダッシュボードへリダイレクト
                    else:
                         return redirect('dashboard')
                else:
                    form.add_error('code', '認証コードが正しくないか、有効期限が切れています。')

            except LoginRequest.DoesNotExist:
                 return redirect('request_login_code')

        return render(request, 'accounts/verify_code.html', {'form': form, 'email': email})

# --- プロフィール更新ページ (初回ログイン時など) ---
@login_required_custom
def profile_update_view(request):
    login_request_id = request.session.get('login_request_id')
    user_profile = get_object_or_404(LoginRequest, id=login_request_id)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user_profile)
        if form.is_valid():
            updated_profile = form.save(commit=False)
            # セッションの役職も更新
            request.session['user_role'] = updated_profile.role 
            updated_profile.is_approved = True # ★ 常に承認済みに
            updated_profile.save()
            
            # ★ 承認待ちのチェックを削除し、ダッシュボードへリダイレクト
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=user_profile)

    return render(request, 'accounts/profile_form.html', {'form': form})


# --- ログアウト処理 ---
def custom_logout(request):
    for key in list(request.session.keys()):
        if not key.startswith('_'):
             del request.session[key]
    return redirect('landing')

# --- トップページ（ランディングページ） ---
class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        if request.session.get('login_request_id'):
            return redirect('dashboard')
        return render(request, 'accounts/landing.html') # ★パスを修正

# --- ダッシュボード (ログイン保護) ---
@login_required_custom
def dashboard_view(request):
    login_request_id = request.session.get('login_request_id')
    login_request = get_object_or_404(LoginRequest, id=login_request_id)
    # ★ 承認待ちのチェックを削除
    return render(request, 'accounts/dashboard.html', {'login_request': login_request})

# --- アカウント一覧 (ログイン保護) ---
@login_required_custom
def account_list_view(request):
    login_request_id = request.session.get('login_request_id')
    my_accounts = LoginRequest.objects.filter(id=login_request_id) # アカウント切り替えは廃止
    context = {'my_accounts': my_accounts}
    return render(request, 'accounts/account_list.html', context)

# --- 承認関連のビュー (wait_for_approval_view, approval_list_view, approve_request) は削除 ---