from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'group', 'phone')
    search_fields = ('email', 'first_name', 'last_name', 'group')
    list_filter = ('group',)
    filter_horizontal = ('skills',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('email', 'first_name', 'last_name', 'phone', 'group'),
        }),
        ('Дополнительная информация', {
            'fields': ('bio', 'skills', 'avatar'),
        }),
        ('Рейтинг', {
            'fields': ('total_rating', 'rated_by_amount'),
        }),
        ('Дата регистрации', {
            'fields': ('created_at',),
        }),
    )
