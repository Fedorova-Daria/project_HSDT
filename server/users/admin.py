from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'group', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')
    filter_horizontal = ('technologies',)  # Это добавит горизонтальный выбор для ManyToMany полей


admin.site.register(UserProfile)

