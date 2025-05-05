from django.contrib import admin
from .models import Team, TeamJoinRequest


@admin.register(Team)
class ProjectAdmin(admin.ModelAdmin):
    model = Team


@admin.register(TeamJoinRequest)
class ProjectAdmin(admin.ModelAdmin):
    model = TeamJoinRequest

