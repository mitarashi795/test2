# schedule/urls.py (新規作成)
from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar_root'),
    path('calendar/<int:year>/<int:month>/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('event/<int:pk>/toggle_completion/', views.toggle_event_completion, name='event_toggle_completion'),
]