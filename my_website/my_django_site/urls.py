"""
URL configuration for my_django_site project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ★ urlpatterns の定義を一つにまとめます
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),      # accounts アプリをルート('')に設定
    path('polls/', include('polls.urls')),      # polls アプリを /polls/ 以下に設定
    path('schedule/', include('schedule.urls')), # schedule アプリを /schedule/ 以下に設定
    # path('accounts/', include('django.contrib.auth.urls')), # ← Django標準認証は使わないので不要
]

# 開発環境でメディアファイルを配信するための設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)