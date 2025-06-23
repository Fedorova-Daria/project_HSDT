from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from teams.models import TeamJoinRequest
from projects.models import ProjectApplication
from notifications.utils import create_notification

# --- TEAM JOIN REQUEST ---

@receiver(post_save, sender=TeamJoinRequest)
def notify_team_join_request_created(sender, instance, created, **kwargs):
    if created:
        create_notification(
            user=instance.team.owner,
            notification_type='team_join_request_sent',
            message=f"{instance.user.get_full_name()} подал(а) заявку в команду {instance.team.name}",
            related_team=instance.team,
            related_team_join_request=instance,
            is_read = False,
        )

@receiver(pre_save, sender=TeamJoinRequest)
def notify_team_join_request_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # новая заявка, не обновляем

    old = TeamJoinRequest.objects.get(pk=instance.pk)
    if old.status != instance.status and instance.status == 'accepted':
        create_notification(
            user=instance.user,
            notification_type='team_join_request_accepted',
            message=f"Ваша заявка в команду {instance.team.name} была принята!",
            related_team=instance.team,
            related_team_join_request=instance,
            is_read = False,
        )

# --- PROJECT APPLICATION ---

@receiver(post_save, sender=ProjectApplication)
def notify_project_application_created(sender, instance, created, **kwargs):
    if created:
        applicant_name = (
            instance.team.name if instance.applicant_type == 'team'
            else instance.freelancer.get_full_name()
        )

        create_notification(
            user=instance.project.initiator,
            notification_type='project_join_request_sent',
            message=f"{applicant_name} подал(а) заявку в проект {instance.project.title}",
            related_project=instance.project,
            related_project_application=instance,
            related_team=instance.team if instance.applicant_type == 'team' else None,
            is_read=False
        )

@receiver(pre_save, sender=ProjectApplication)
def notify_project_application_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # новая заявка

    old = ProjectApplication.objects.get(pk=instance.pk)
    if old.status != instance.status and instance.status == 'accepted':
        recipient = (
            instance.team.owner if instance.applicant_type == 'team'
            else instance.freelancer
        )

        create_notification(
            user=recipient,
            notification_type='project_join_request_accepted',
            message=f"Ваша заявка на участие в проекте {instance.project.title} была принята!",
            related_project=instance.project,
            related_project_application=instance,
            related_team=instance.team if instance.applicant_type == 'team' else None,
            is_read = False,
        )