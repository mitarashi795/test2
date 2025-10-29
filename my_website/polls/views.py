# polls/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponseForbidden
import json

from .models import Poll, Question, Choice, Answer
from accounts.models import LoginRequest
from .forms import PollForm

# 投票一覧ページ
class PollListView(ListView):
    model = Poll
    template_name = 'polls/poll_list.html'
    ordering = ['-created_at']

# 投票作成ページ
class PollCreateView(UserPassesTestMixin, CreateView):
    model = Poll
    form_class = PollForm
    template_name = 'polls/poll_form.html'

    def form_valid(self, form):
        # フォームが送信される前に、作成者情報を追加する
        login_request_id = self.request.session.get('login_request_id')
        current_user = get_object_or_404(LoginRequest, id=login_request_id)
        form.instance.created_by = current_user
        return super().form_valid(form)

    def get_success_url(self):
        # 保存成功後は質問追加ページに移動
        return reverse_lazy('add_question', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        # 実行委員長または委員長のみが作成可能
        role = self.request.session.get('user_role')
        return role in ['実行委員長', '委員長']

# 質問追加ページ
def add_question_to_poll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '').strip()
        question_type = request.POST.get('question_type')
        # 「計算する」チェックボックスの値を取得
        calculate_sum = request.POST.get('calculate_sum') == 'on'

        if not question_text:
            context = {'poll': poll, 'error': '質問文を入力してください。'}
            return render(request, 'polls/add_question_form.html', context)
        
        # バリデーション通過後に、保存処理を行う
        question = Question.objects.create(
            poll=poll, 
            text=question_text, 
            question_type=question_type,
            calculate_sum=calculate_sum
        )
        
        if question_type == 'CHOICE':
            choices_text = request.POST.getlist('choice_text')
            valid_choices = [c.strip() for c in choices_text if c.strip()]
            
            if not valid_choices:
                question.delete() 
                context = {'poll': poll, 'error': '選択式の質問には、少なくとも1つの選択肢を入力してください。'}
                return render(request, 'polls/add_question_form.html', context)
            else:
                for choice_text in valid_choices:
                    Choice.objects.create(question=question, text=choice_text)

        if 'add_another' in request.POST:
            return redirect('add_question', pk=poll.pk)
        else:
            return redirect('poll_list')

    return render(request, 'polls/add_question_form.html', {'poll': poll})
    
# 投票詳細・投票ページ
def poll_detail_view(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    login_request_id = request.session.get('login_request_id')
    
    context = {'poll': poll}
    
    if not login_request_id:
        context['error'] = 'ログインしてください。'
        return render(request, 'polls/poll_detail.html', context)

    current_user = get_object_or_404(LoginRequest, id=login_request_id)

    if request.method == 'POST':
        for question in poll.questions.all():
            if question.question_type == 'CHOICE':
                choice_id = request.POST.get(f'question_{question.id}')
                if choice_id:
                    choice = get_object_or_404(Choice, id=choice_id)
                    Answer.objects.create(question=question, user=current_user, choice=choice)
            elif question.question_type == 'TEXT':
                text_answer = request.POST.get(f'question_{question.id}')
                if text_answer:
                    Answer.objects.create(question=question, user=current_user, text_answer=text_answer)
            elif question.question_type == 'PHOTO':
                image_answer = request.FILES.get(f'question_{question.id}')
                if image_answer:
                    Answer.objects.create(question=question, user=current_user, image_answer=image_answer)
        
        return redirect('poll_list')

    return render(request, 'polls/poll_detail.html', context)

# --- 自分が作成した投票の管理ページ ---
class PollManageListView(UserPassesTestMixin, ListView):
    model = Poll
    template_name = 'polls/poll_manage_list.html'

    def get_queryset(self):
        login_request_id = self.request.session.get('login_request_id')
        if not login_request_id:
            return Poll.objects.none()
        current_user = get_object_or_404(LoginRequest, id=login_request_id)
        return Poll.objects.filter(created_by=current_user).order_by('-created_at')

    def test_func(self):
        role = self.request.session.get('user_role')
        return role in ['実行委員長', '委員長']

# --- 投票結果の表示ページ ---
class PollResultsView(UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=pk)
        
        voter_roles = set()
        for question in poll.questions.all():
            for answer in question.answer_set.all():
                voter_roles.add(answer.user.display_role)
        
        sorted_voter_roles = sorted(list(voter_roles))

        context = {
            'poll': poll,
            'voter_roles': sorted_voter_roles,
        }
        return render(request, 'polls/poll_results.html', context)

    def test_func(self):
        poll = self.get_object()
        login_request_id = self.request.session.get('login_request_id')
        if not login_request_id: return False
        current_user = get_object_or_404(LoginRequest, id=login_request_id)
        return poll.created_by == current_user
    
    def get_object(self):
        return get_object_or_404(Poll, pk=self.kwargs.get('pk'))

# --- 投票設定の変更ページ (poll_edit) ---
class PollSettingsUpdateView(UserPassesTestMixin, UpdateView):
    model = Poll
    fields = ['title', 'description']
    template_name = 'polls/poll_form.html'
    
    def get_success_url(self):
        # 編集後は管理詳細ページに戻る
        return reverse_lazy('poll_manage_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        poll = self.get_object()
        login_request_id = self.request.session.get('login_request_id')
        if not login_request_id: return False
        current_user = get_object_or_404(LoginRequest, id=login_request_id)
        return poll.created_by == current_user

# --- 質問の削除ビュー ---
class QuestionDeleteView(UserPassesTestMixin, View):
    def post(self, request, pk, *args, **kwargs):
        question = get_object_or_404(Question, pk=pk)
        poll_id = question.poll.id
        question.delete()
        return redirect('poll_manage_detail', pk=poll_id)

    def test_func(self):
        question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        login_request_id = self.request.session.get('login_request_id')
        if not login_request_id: return False
        current_user = get_object_or_404(LoginRequest, id=login_request_id)
        return question.poll.created_by == current_user

# --- 選択肢の編集ビュー ---
def manage_choices_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    
    ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('text',), extra=1, can_delete=True)

    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST, instance=question)
        if formset.is_valid():
            poll_id = question.poll.id 
            formset.save()
            
            if not question.choices.exists():
                question.delete() 
            
            return redirect('poll_manage_detail', pk=poll_id)
    else:
        formset = ChoiceFormSet(instance=question)
        
    return render(request, 'polls/manage_choices.html', {'formset': formset, 'question': question})

# --- 管理詳細ページ用の新しいビュー ---
class PollManageDetailView(UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=pk)
        return render(request, 'polls/poll_manage_detail.html', {'poll': poll})

    def test_func(self):
        poll = get_object_or_404(Poll, pk=self.kwargs.get('pk'))
        login_request_id = self.request.session.get('login_request_id')
        if not login_request_id: return False
        current_user = get_object_or_404(LoginRequest, id=login_request_id)
        return poll.created_by == current_user