from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class ProjectAdmin(admin.ModelAdmin):
    model = Notification


