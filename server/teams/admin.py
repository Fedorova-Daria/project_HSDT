from django.contrib import admin
from .models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_members', 'privacy')
    search_fields = ('name', 'description')
    list_filter = ('privacy',)


admin.site.register(Team, TeamAdmin)

