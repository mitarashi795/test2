# schedule/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
import calendar
from .models import Event
from .forms import EventForm
from accounts.models import LoginRequest
from django.http import HttpResponseRedirect

# ★ ログイン保護デコレータをインポート
from accounts.views import login_required_custom
from django.utils.decorators import method_decorator

# --- 権限チェック用のMixin ---
@method_decorator(login_required_custom, name='dispatch') # ★クラス自体も保護
class CalendarPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        role = self.request.session.get('user_role')
        return role in ['実行委員長', '委員長', '教員']

# --- カレンダー表示ビュー ---
class CalendarView(CalendarPermissionMixin, View):
    def get(self, request, year=None, month=None, *args, **kwargs):
        if year is None or month is None:
            today = timezone.now().astimezone(timezone.get_current_timezone())
            return redirect('calendar', year=today.year, month=today.month)
        cal = calendar.Calendar()
        month_dates = cal.monthdatescalendar(year, month)
        # ★ .filter() を修正。カレンダーに表示するイベントは、その月に「終了」するもの
        events = Event.objects.filter(end_time__year=year, end_time__month=month)
        current_month = timezone.datetime(year, month, 1)
        prev_month = current_month - timezone.timedelta(days=1)
        next_month = current_month + timezone.timedelta(days=31)
        context = {
            'month_dates': month_dates, 'year': year, 'month': month,
            'month_name': current_month.strftime('%Y年 %m月'),
            'events': events,
            'prev_year': prev_month.year, 'prev_month': prev_month.month,
            'next_year': next_month.year, 'next_month': next_month.month,
        }
        return render(request, 'schedule/calendar.html', context)

# --- イベント作成ビュー ---
class EventCreateView(CalendarPermissionMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'schedule/event_form.html'
    def form_valid(self, form):
        login_request_id = self.request.session.get('login_request_id')
        current_user = get_object_or_404(LoginRequest, id=login_request_id)
        form.instance.created_by = current_user
        return super().form_valid(form)
    def get_success_url(self):
        start_time = self.object.start_time.astimezone(timezone.get_current_timezone())
        return reverse_lazy('calendar', kwargs={'year': start_time.year, 'month': start_time.month})

# --- イベント編集ビュー ---
@method_decorator(login_required_custom, name='dispatch') # ★保護デコレータを追加
class EventUpdateView(UserPassesTestMixin, UpdateView): 
    model = Event
    form_class = EventForm
    template_name = 'schedule/event_form.html'
    def test_func(self):
        role = self.request.session.get('user_role')
        if role not in ['実行委員長', '委員長', '教員']:
            return False
        event = self.get_object()
        login_request_id = self.request.session.get('login_request_id')
        if not login_request_id:
            return False
        return event.created_by_id == login_request_id
    def get_success_url(self):
        start_time = self.object.start_time.astimezone(timezone.get_current_timezone())
        return reverse_lazy('calendar', kwargs={'year': start_time.year, 'month': start_time.month})

# --- イベント削除ビュー ---
@method_decorator(login_required_custom, name='dispatch') # ★保護デコレータを追加
class EventDeleteView(UserPassesTestMixin, DeleteView): 
    model = Event
    template_name = 'schedule/event_confirm_delete.html'
    def test_func(self):
        role = self.request.session.get('user_role')
        if role not in ['実行委員長', '委員長', '教員']:
            return False
        event = self.get_object()
        login_request_id = self.request.session.get('login_request_id')
        if not login_request_id:
            return False
        return event.created_by_id == login_request_id
    def get_success_url(self):
        start_time = self.object.start_time.astimezone(timezone.get_current_timezone())
        return reverse_lazy('calendar', kwargs={'year': start_time.year, 'month': start_time.month})

# --- イベント完了/未完了トグルビュー ---
@login_required_custom # ★保護デコレータを追加
def toggle_event_completion(request, pk):
    event = get_object_or_404(Event, pk=pk)
    login_request_id = request.session.get('login_request_id')
    if request.method == 'POST' and event.created_by_id == login_request_id:
        event.completed = not event.completed
        event.save()
        return HttpResponseRedirect(reverse_lazy('event_edit', kwargs={'pk': event.pk}))
    start_time = event.start_time.astimezone(timezone.get_current_timezone())
    return redirect('calendar', year=start_time.year, month=start_time.month)