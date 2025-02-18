from django.contrib import admin
from .models import Project
from .models import Idea
from .models import Team


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name", "description")
    filter_horizontal = ('technologies',)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name", "description")
    filter_horizontal = ('technologies', 'likes')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_private", "created_at")
    search_fields = ("name", "description")
    filter_horizontal = ('members',)

