from django.db import models
from users.models import Account
from django.conf import settings

class Team(models.Model):
    STATUS_CHOICES = [
        ("open", "Открыта"),
        ("private", "Приватная"),
        ('in_progress', 'В работе'),
        ('over', "Распалась") # !!!
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    members = models.ManyToManyField(Account, related_name="teams", blank=True)
    avatar = models.ImageField(upload_to="team_avatars/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    disbanded_at = models.DateTimeField(null=True, blank=True) # !!!

    projects = models.ManyToManyField('projects.Project', related_name="teams_working_on", blank=True) # !!!
    ideas = models.ManyToManyField('projects.Idea', related_name="teams_working_on_ideas", blank=True) # !!!

    class Meta: # Пользователь может создать еще одну команду, если прошлая его уже распалась!!!

        constraints = [ # !!!
            models.UniqueConstraint( # !!!
                fields=['owner'],
                condition=models.Q(status__in=['active', 'private','in_progress']), # !!!
                name='unique_active_team_per_owner' # !!!
            ) # !!!
        ] # !!!

    def __str__(self):
        return self.name

    def can_create_idea(self): # !!!
        return self.status == "private" # !!!

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