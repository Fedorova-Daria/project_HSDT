from django.contrib import admin
from .models import Technology


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Указываем, какие поля показывать в списке
    search_fields = ('name',)  # Добавляем возможность поиска по названию


admin.site.register(Technology, TechnologyAdmin)

