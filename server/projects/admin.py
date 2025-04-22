from django.contrib import admin
from .models import Project, Idea, ProjectApplication


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project

@admin.register(Idea)
class ProjectAdmin(admin.ModelAdmin):
    model = Idea

@admin.register(ProjectApplication)
class ProjectAdmin(admin.ModelAdmin):
    model = Idea

