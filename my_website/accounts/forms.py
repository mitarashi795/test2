# accounts/forms.py (全体を置き換え)
from django import forms

# 役職の選択肢を更新
ROLE_CHOICES = [
    ('教員', '教員'),
    ('実行委員長', '実行委員長'),
    ('委員長', '委員長'),
    ('部活動関係者', '部活動関係者'),    # 「その他」から変更
    ('クラス展示関係者', 'クラス展示関係者'), # 新しく追加
]

# 委員会の選択肢
COMMITTEE_CHOICES = [
    ('', '選択してください'),
    ('企画', '企画'), ('会計', '会計'), ('音響', '音響'),
    ('装飾', '装飾'), ('展示', '展示'), ('広報', '広報'),
    ('模擬店', '模擬店'), ('交通', '交通'), ('若潮丸', '若潮丸'),
    ('本郷C連携', '本郷C連携'),
]

# ★★★ ここに部活動のリストを追加・編集してください ★★★
CLUB_CHOICES = [
    ('', '選択してください'),
    ('柔道', '柔道'),
    ('サッカー', 'サッカー'),
    ('卓球', '卓球'),
    ('テニス', 'テニス'),
    ('バドミントン', 'バドミントン'),
    ('バレーボール', 'バレーボール'),
    ('野球', '野球'),
    ('ラグビー', 'ラグビー'),
    ('陸上', '陸上'),
    ('バスケットボール', 'バスケットボール'),
    ('剣道', '剣道'),
    ('水泳', '水泳'),
    ('カッター', 'カッター'),
    ('ヨット', 'ヨット'),
    ('ダンス', 'ダンス'),
    ('吹奏楽', '吹奏楽'),
    ('軽音楽', '軽音楽'),
    ('茶道', '茶道'),
    ('美術', '美術'),
    ('デジタルメディア創作', 'デジタルメディア創作'),
    ('新聞', '新聞'),
    ('メカトロ技術研究', 'メカトロ技術研究'),
    ('アントレプレナー研究', 'アントレプレナー研究'),
    ('文芸', '文芸'),
    ('機関学', '機関学'),
    ('書道', '書道'),
]

# ★★★ ここにクラス展示のリストを追加・編集してください ★★★
CLASS_EXHIBIT_CHOICES = [
    ('', '選択してください'),
    ('S1', 'S1'),
    ('K1', 'K1'),
    ('I1', 'I1'),
    ('S2', 'S2'),
    ('K2', 'K2'),
    ('I2', 'I2'),
    ('S3', 'S3'),
    ('K3', 'K3'),
    ('I3', 'I3'),
    ('S4', 'S4'),
    ('K4', 'K4'),
    ('I4', 'I4'),
    ('S5', 'S5'),
    ('K5', 'K5'),
    ('I5', 'I5'),
    ('専攻科', '専攻科'),
]


class CustomLoginForm(forms.Form):
    role = forms.ChoiceField(label='役職', choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    committee = forms.ChoiceField(label='所属委員会', choices=COMMITTEE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    
    # ★新しいフォーム項目を追加
    club = forms.ChoiceField(label='所属部活動', choices=CLUB_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    class_exhibit = forms.ChoiceField(label='担当クラス', choices=CLASS_EXHIBIT_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    name = forms.CharField(label='氏名', max_length=100, widget=forms.TextInput(attrs={'placeholder': '例: 山田 太郎'}))
    email = forms.EmailField(label='メールアドレス', widget=forms.EmailInput(attrs={'placeholder': '例: example@school.ac.jp'}))

# accounts/forms.py (ファイルの末尾に追加)
class EmailForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', widget=forms.EmailInput(attrs={'placeholder': '登録済みのメールアドレス'}))

class VerifyCodeForm(forms.Form):
    code = forms.CharField(label='認証コード', max_length=6, min_length=6, widget=forms.TextInput(attrs={'inputmode': 'numeric', 'autocomplete': 'one-time-code'}))