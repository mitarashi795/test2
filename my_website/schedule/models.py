# schedule/models.py
from django.db import models
from django.urls import reverse

class Event(models.Model):
    title = models.CharField("イベント名", max_length=200)
    description = models.TextField("詳細", blank=True)
    start_time = models.DateTimeField("開始日時")
    end_time = models.DateTimeField("終了日時")
    created_by = models.ForeignKey('accounts.LoginRequest', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="作成者")
    # ★ Add this line
    completed = models.BooleanField("完了", default=False)

    def get_absolute_url(self):
        # ★ Change this to point to the edit view
        return reverse('event_edit', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title