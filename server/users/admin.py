from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'group', 'phone', 'rating')
    search_fields = ('email', 'first_name', 'last_name', 'group')
    list_filter = ('group', 'rating')


admin.site.register(Account, AccountAdmin)