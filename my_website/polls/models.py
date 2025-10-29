# polls/models.py
from django.db import models

class Poll(models.Model):
    title = models.CharField("投票のタイトル", max_length=200)
    description = models.TextField("説明", blank=True)
    created_by = models.ForeignKey('accounts.LoginRequest', on_delete=models.CASCADE, verbose_name="作成者")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# polls/models.py

class Question(models.Model):
    QUESTION_TYPES = [
        ('CHOICE', '選択式'),
        ('TEXT', '文字入力'),
        ('PHOTO', '写真アップロード'),
    ]
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField("質問文", max_length=255)
    question_type = models.CharField("質問タイプ", max_length=10, choices=QUESTION_TYPES)
    
    # ★この行を新しく追加
    calculate_sum = models.BooleanField("合計を計算する", default=False)

    def __str__(self):
        return self.text

# polls/models.py

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField("選択肢", max_length=100)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.LoginRequest', on_delete=models.CASCADE)
    # 回答はどれか1つだけが入る
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)
    image_answer = models.ImageField(upload_to='answers/', null=True, blank=True)