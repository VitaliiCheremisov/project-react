from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

admin.site.empty_value_display = '-пусто-'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
