from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SettleUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')


admin.site.register(SettleUser, CustomUserAdmin)
