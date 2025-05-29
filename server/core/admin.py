from django.contrib import admin
from .models import Technology, UniversityGroup, Semester


admin.site.register(Technology)
admin.site.register(UniversityGroup)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('year', 'semester')
    list_filter = ('year', 'semester')
    ordering = ('-year', 'semester')