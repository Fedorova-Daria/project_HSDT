from teams.models import Team
from projects.models import ProjectApplication

def create_notification(
    user,  # кому отправляется
    notification_type,
    message=None,
    related_team=None,
    related_project=None,
    related_team_join_request=None,
    related_project_application=None
):
    from .models import Notification

    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        message=message,
        related_team=related_team,
        related_project=related_project,
        related_team_join_request=related_team_join_request,
        related_project_application=related_project_application
    )

# 🔹 TEAM_REQUEST шаблоны
"""def notify_team_join_requested(team_owner, join_request):
    create_notification(
        user=team_owner,
        notification_type=Notification.NotificationType.TEAM_REQUEST,
        message=f"{join_request.user} подал(а) заявку в команду «{join_request.team.name}».",
        related_team_join_request=join_request
    )

def notify_team_join_accepted(user, team, join_request):
    create_notification(
        user=user,
        notification_type=Notification.NotificationType.TEAM_REQUEST,
        message=f"Ваша заявка в команду «{team.name}» была принята.",
        related_team_join_request=join_request
    )

def notify_team_join_declined(user, team, join_request):
    create_notification(
        user=user,
        notification_type=Notification.NotificationType.TEAM_REQUEST,
        message=f"Ваша заявка в команду «{team.name}» была отклонена.",
        related_team_join_request=join_request
    )

# 🔹 PROJECT_REQUEST шаблоны

def notify_project_application_submitted(project_owner, application):
    create_notification(
        user=project_owner,
        notification_type=Notification.NotificationType.PROJECT_REQUEST,
        message=f"{application.user} хочет присоединиться к проекту «{application.project.title}».",
        related_project_application=application
    )

def notify_project_application_accepted(user, project, application):
    create_notification(
        user=user,
        notification_type=Notification.NotificationType.PROJECT_REQUEST,
        message=f"Ваша заявка на участие в проекте «{project.title}» была принята.",
        related_project_application=application
    )

def notify_project_application_declined(user, project, application):
    create_notification(
        user=user,
        notification_type=Notification.NotificationType.PROJECT_REQUEST,
        message=f"Ваша заявка на участие в проекте «{project.title}» была отклонена.",
        related_project_application=application
    )

# 🔹 SYSTEM (по желанию)

def notify_system(user, message):
    create_notification(
        user=user,
        notification_type=Notification.NotificationType.SYSTEM,
        message=message
    )"""