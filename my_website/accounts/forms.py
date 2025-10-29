# accounts/forms.py (この内容で全体を置き換えてください)
from django import forms
from .models import LoginRequest # ★ LoginRequestをインポート

# 役職の選択肢を更新
ROLE_CHOICES = [
    ('教員', '教員'),
    ('実行委員長', '実行委員長'),
    ('委員長', '委員長'),
    ('部活動関係者', '部活動関係者'),
    ('クラス展示関係者', 'クラス展示関係者'),
]

# 委員会の選択肢
COMMITTEE_CHOICES = [
    ('', '選択してください'),
    ('企画', '企画'), ('会計', '会計'), ('音響', '音響'),
    ('装飾', '装飾'), ('展示', '展示'), ('広報', '広報'),
    ('模擬店', '模擬店'), ('交通', '交通'), ('若潮丸', '若潮丸'),
    ('本郷C連携', '本郷C連携'),
]

# 部活動のリスト
CLUB_CHOICES = [
    ('', '選択してください'),
    ('柔道', '柔道'), ('サッカー', 'サッカー'), ('卓球', '卓球'),
    ('テニス', 'テニス'), ('バドミントン', 'バドミントン'), ('バレーボール', 'バレーボール'),
    ('野球', '野球'), ('ラグビー', 'ラグビー'), ('陸上', '陸上'),
    ('バスケットボール', 'バスケットボール'), ('剣道', '剣道'), ('水泳', '水泳'),
    ('カッター', 'カッター'), ('ヨット', 'ヨット'), ('ダンス', 'ダンス'),
    ('吹奏楽', '吹奏楽'), ('軽音楽', '軽音楽'), ('茶道', '茶道'),
    ('美術', '美術'), ('デジタルメディア創作', 'デジタルメディア創作'), ('新聞', '新聞'),
    ('メカトロ技術研究', 'メカトロ技術研究'), ('アントレプレナー研究', 'アントレプレナー研究'),
    ('文芸', '文芸'), ('機関学', '機関学'), ('書道', '書道'),
]

# クラス展示のリスト
CLASS_EXHIBIT_CHOICES = [
    ('', '選択してください'),
    ('S1', 'S1'), ('K1', 'K1'), ('I1', 'I1'),
    ('S2', 'S2'), ('K2', 'K2'), ('I2', 'I2'),
    ('S3', 'S3'), ('K3', 'K3'), ('I3', 'I3'),
    ('S4', 'S4'), ('K4', 'K4'), ('I4', 'I4'),
    ('S5', 'S5'), ('K5', 'K5'), ('I5', 'I5'),
    ('専攻科', '専攻科'),
]

# ★ CustomLoginForm は削除

# メールアドレス入力フォーム
class EmailForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', widget=forms.EmailInput(attrs={'placeholder': '登録済みのメールアドレス', 'class': 'form-control'}))

# コード検証フォーム
class VerifyCodeForm(forms.Form):
    code = forms.CharField(label='認証コード (6桁)', max_length=6, min_length=6, widget=forms.TextInput(attrs={'inputmode': 'numeric', 'autocomplete': 'one-time-code', 'class': 'form-control'}))

# ★ 初回プロフィール更新用フォーム
class ProfileUpdateForm(forms.ModelForm):
    role = forms.ChoiceField(label='役職', choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    committee = forms.ChoiceField(label='所属委員会', choices=COMMITTEE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    club = forms.ChoiceField(label='所属部活動', choices=CLUB_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    class_exhibit = forms.ChoiceField(label='担当クラス', choices=CLASS_EXHIBIT_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = LoginRequest
        fields = ['name', 'role', 'committee', 'club', 'class_exhibit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }