# polls/urls.py (修正)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PollListView.as_view(), name='poll_list'),
    path('create/', views.PollCreateView.as_view(), name='poll_create'),
    path('<int:pk>/', views.poll_detail_view, name='poll_detail'),
    path('<int:pk>/add_question/', views.add_question_to_poll, name='add_question'),
    path('manage/', views.PollManageListView.as_view(), name='poll_manage_list'),
    path('<int:pk>/results/', views.PollResultsView.as_view(), name='poll_results'),
    
    # ★PollUpdateViewを新しい名前に変更
    path('<int:pk>/edit/', views.PollSettingsUpdateView.as_view(), name='poll_edit'),

    # ★ここから新しいURLを追加
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('question/<int:pk>/choices/', views.manage_choices_view, name='manage_choices'),
    path('<int:pk>/manage/', views.PollManageDetailView.as_view(), name='poll_manage_detail'),
]