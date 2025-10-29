# accounts/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta

class LoginRequest(models.Model):
    ROLE_CHOICES = [
        ('教員', '教員'),
        ('実行委員長', '実行委員長'),
        ('委員長', '委員長'),
        ('部活動関係者', '部活動関係者'),
        ('クラス展示関係者', 'クラス展示関係者'),
    ]

    name = models.CharField("氏名", max_length=100)
    # ★★★ ここに unique=True を追加 ★★★
    email = models.EmailField("メールアドレス", unique=True)
    
    role = models.CharField("役職", max_length=50, choices=ROLE_CHOICES)
    committee = models.CharField("所属委員会", max_length=50, blank=True, null=True)
    club = models.CharField("所属部活動", max_length=50, blank=True, null=True)
    class_exhibit = models.CharField("担当クラス", max_length=50, blank=True, null=True)
    is_approved = models.BooleanField("承認済み", default=False)
    timestamp = models.DateTimeField("ログイン日時", auto_now_add=True)

    otp_code_hash = models.CharField("OTPハッシュ", max_length=128, blank=True, null=True)
    otp_expiry = models.DateTimeField("OTP有効期限", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role}) - {'承認済み' if self.is_approved else '未承認'}"

    @property
    def display_role(self):
        if self.role == '委員長' and self.committee:
            return f"{self.role}({self.committee})"
        elif self.role == '部活動関係者' and self.club:
            return f"{self.role}({self.club})"
        elif self.role == 'クラス展示関係者' and self.class_exhibit:
            return f"{self.role}({self.class_exhibit})"
        return self.role