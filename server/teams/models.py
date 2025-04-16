from django.db import models
from users.models import Account
from django.conf import settings


class Team(models.Model):
    STATUS_CHOICES = [
        ("open", "Открыта"),
        ("private", "Приватная"),
        ('in_progress', 'В работе'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    owner = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="owned_team")
    members = models.ManyToManyField(Account, related_name="teams", blank=True)
    avatar = models.ImageField(upload_to="team_avatars/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    def __str__(self):
        return self.name


class TeamJoinRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает'),
        ('accepted', 'Принят'),
        ('declined', 'Отклонён'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team_join_requests")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="join_requests")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'team')

'''
class TeamProjectRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    score = models.PositiveIntegerField()  # 0-100
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

'''