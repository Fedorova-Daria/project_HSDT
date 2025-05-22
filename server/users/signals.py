from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from teams.models import Team
from projects.models import Project
from .models import UserActivity
from django.utils.timezone import now

# --- Сигнал для изменений участников команды ---
@receiver(m2m_changed, sender=Team.members.through)
def team_members_changed(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            # Создаём UserActivity только если нет активной записи
            if not UserActivity.objects.filter(user_id=user_id, team=instance, ended_at__isnull=True).exists():
                UserActivity.objects.create(
                    user_id=user_id,
                    team=instance,
                    started_at=now()
                )
    elif action == "post_remove":
        for user_id in pk_set:
            try:
                ua = UserActivity.objects.filter(user_id=user_id, team=instance, ended_at__isnull=True).latest('started_at')
                ua.ended_at = now()
                ua.save()
            except UserActivity.DoesNotExist:
                pass

# --- Сигнал для изменений фрилансеров проекта ---
@receiver(m2m_changed, sender=Project.workers.through)
def project_workers_changed(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            if not UserActivity.objects.filter(user_id=user_id, project=instance, ended_at__isnull=True).exists():
                UserActivity.objects.create(
                    user_id=user_id,
                    project=instance,
                    started_at=now()
                )
    elif action == "post_remove":
        for user_id in pk_set:
            try:
                ua = UserActivity.objects.filter(user_id=user_id, project=instance, ended_at__isnull=True).latest('started_at')
                ua.ended_at = now()
                ua.save()
            except UserActivity.DoesNotExist:
                pass

# --- Сигнал для изменений команд в проекте ---
@receiver(m2m_changed, sender=Project.teams.through)
def project_teams_changed(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for team_id in pk_set:
            team = Team.objects.get(id=team_id)
            for user in team.members.all():
                if not UserActivity.objects.filter(user=user, project=instance, ended_at__isnull=True).exists():
                    UserActivity.objects.create(
                        user=user,
                        project=instance,
                        started_at=now()
                    )
    elif action == "post_remove":
        for team_id in pk_set:
            team = Team.objects.get(id=team_id)
            for user in team.members.all():
                try:
                    ua = UserActivity.objects.filter(user=user, project=instance, ended_at__isnull=True).latest('started_at')
                    ua.ended_at = now()
                    ua.save()
                except UserActivity.DoesNotExist:
                    pass

# --- Сигнал при сохранении проекта ---
@receiver(post_save, sender=Project)
def project_status_changed(sender, instance, **kwargs):
    if instance.status == "done":
        # Собираем всех пользователей проекта: workers + все участники команд
        user_ids = set(instance.workers.values_list('id', flat=True))
        for team in instance.teams.all():
            user_ids.update(team.members.values_list('id', flat=True))

        for user_id in user_ids:
            try:
                ua = UserActivity.objects.filter(user_id=user_id, project=instance, ended_at__isnull=True).latest('started_at')
                ua.ended_at = now()
                ua.save()
            except UserActivity.DoesNotExist:
                pass