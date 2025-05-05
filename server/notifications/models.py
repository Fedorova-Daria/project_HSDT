from django.db import models
from users.models import Account  # Импортируем модель пользователя Account
from projects.models import Project, Idea, ProjectApplication
from teams.models import Team, TeamJoinRequest


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        TEAM_REQUEST = 'team_request', 'Запрос в команду'
        PROJECT_REQUEST = 'project_request', 'Запрос в проект'
        SYSTEM = 'system', 'Системное уведомление'

    type = models.CharField(max_length=50, choices=NotificationType.choices)
    message = models.TextField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    related_team_join_request = models.ForeignKey(TeamJoinRequest, on_delete=models.SET_NULL, null=True, blank=True)
    related_project_application = models.ForeignKey(ProjectApplication, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.type


