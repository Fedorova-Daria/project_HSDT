from django.contrib import admin
from .models import Project, Idea, ProjectApplication, ProjectMessage
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect, render
from django.contrib import messages
from core.models import Semester
import json
from notifications.models import Notification

class SemesterYearFilter(admin.SimpleListFilter):
    title = 'Год'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = Semester.objects.order_by('-year').values_list('year', flat=True).distinct()
        return [(year, str(year)) for year in years]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(semester__year=self.value())
        return queryset


class SemesterNameFilter(admin.SimpleListFilter):
    title = 'Семестр'
    parameter_name = 'semester_name'

    def lookups(self, request, model_admin):
        year = request.GET.get('year')
        if not year:
            return []  # Если год не выбран, семестры не показываем
        semesters = Semester.objects.filter(year=year).order_by('semester')
        return [(s.semester, s.get_semester_display()) for s in semesters]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(semester__semester=self.value())
        return queryset

class InstituteFilter(admin.SimpleListFilter):
    title = 'Институт'
    parameter_name = 'institute'

    INSTITUTE_CHOICES = [
        ('HSDT', 'ВШЦТ'),
        ('ARHID', 'АРХИД'),
        ('IPTI', 'ИПТИ'),
        ('STROIN', 'СТРОИН'),
    ]

    def lookups(self, request, model_admin):
        return self.INSTITUTE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            # Фильтруем проекты, у которых в поле institutes есть выбранный код
            # Т.к. это JSON-строка, используем __contains
            # но это работает как поиск подстроки, поэтому фильтр может быть неточным
            code = self.value()
            return queryset.filter(institutes__contains=code)
        return queryset

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'visible', 'initiator', 'semester']
    list_filter = [SemesterYearFilter, SemesterNameFilter, 'status', 'visible', InstituteFilter]
    # Определяем, какие поля будут отображаться на странице редактирования
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'status', 'visible', 'initiator', 'skills_required', 'display_institutes', 'semester')
        }),
    )

    readonly_fields = ['title', 'status', 'visible', 'initiator', 'skills_required', 'display_institutes']

    @admin.display(description='Институты')
    def display_institutes(self, obj):
        return ", ".join(obj.institutes_verbose)

    # + кнопки Confirm и Revise
    change_form_template = 'admin/project_change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:project_id>/confirm/', self.admin_site.admin_view(self.confirm_project), name='project-confirm'),
            path('<int:project_id>/revise/', self.admin_site.admin_view(self.send_to_revision), name='project-revise'),
        ]
        return custom_urls + urls

    def confirm_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Подтвердить проверку</a>',
            f'{obj.id}/confirm/'
        )
    confirm_button.short_description = "Подтвердить"

    def send_revision_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Отправить на доработку</a>',
            f'{obj.id}/revise/'
        )
    send_revision_button.short_description = "Доработка"

    def confirm_project(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        project.status = 'review'
        project.save()
        messages.success(request, 'Проект подтверждён.')
        return redirect(f'/admin/projects/project/{project_id}/change/')

    def send_to_revision(self, request, project_id):
        project = Project.objects.get(pk=project_id)

        if request.method == 'POST':
            text = request.POST.get('message')
            if text:
                ProjectMessage.objects.create(
                    project=project,
                    sender=request.user,
                    text=text,
                    is_revision_request=True,
                    sender_role = 'admin'
                )
                project.status = 'under_revision_on_admin'
                project.save()

            # Создаем уведомление для инициатора
            initiator = project.initiator
            if initiator:
                Notification.objects.create(
                    notification_type='project_on_under_revision',
                    message=f'Проект "{project.title}" отправлен на доработку с сообщением',
                    user=initiator,
                    related_project=project,
                )

                messages.success(request, 'Сообщение отправлено, проект на доработке.')
                return redirect(f'/admin/projects/project/{project_id}/change/')
            else:
                messages.error(request, 'Сообщение не может быть пустым.')

        return render(request, 'admin/send_revision.html', {
            'project': project
        })


@admin.register(Idea)
class ProjectAdmin(admin.ModelAdmin):
    model = Idea

@admin.register(ProjectApplication)
class ProjectApplicationAdmin(admin.ModelAdmin):
    model = Idea

