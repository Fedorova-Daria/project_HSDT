from django.db import models
from users.models import Account  # Импортируем модель пользователя Account
from projects.models import Project, Idea, ProjectApplication
from teams.models import Team, TeamJoinRequest


class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ('team_join_request_sent', 'Заявка в команду отправлена'),
        ('team_join_request_accepted', 'Заявка в команду принята'),
        ('added_to_team', 'Добавление в команду'),
        ('project_join_request_sent', 'Заявка в проект отправлена'),
        ('project_join_request_accepted', 'Заявка в проект принята'),
        ('system', 'Системное уведомление'), 
        ('project_on_under_revision', 'Проект отправлен на доработку')
        # добавь любые другие типы
    )

    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='info')
    message = models.TextField(null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    related_team = models.ForeignKey('teams.Team', null=True, blank=True, on_delete=models.CASCADE)
    related_project = models.ForeignKey('projects.Project', null=True, blank=True, on_delete=models.CASCADE)
    related_team_join_request = models.ForeignKey(TeamJoinRequest, on_delete=models.SET_NULL, null=True, blank=True)
    related_project_application = models.ForeignKey(ProjectApplication, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.notification_type


