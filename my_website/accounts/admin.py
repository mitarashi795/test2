# accounts/admin.py
from django.contrib import admin
from .models import LoginRequest

admin.site.register(LoginRequest)