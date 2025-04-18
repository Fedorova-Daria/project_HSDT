from django.db import models
from users.models import Account
from core.models import Technology
from teams.models import Team


class Project(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('review', 'На рассмотрении'),
        ('open', 'В поиске'),
        ('in_progress', 'В работе'),
        ('done', 'Сделан'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.ManyToManyField(Technology, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='projects_owned')
    initiator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='projects_initiated')
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='projects_customer')

    applicants = models.ManyToManyField(Account, related_name="applied_projects", blank=True)
    workers = models.ManyToManyField(Account, related_name="working_on_projects", blank=True)
    selected_team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects"
    )
    favorites = models.ManyToManyField(Account, related_name="favorite_projects", blank=True)
    experts_voted = models.ManyToManyField(Account, related_name="voted_projects", blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    visible = models.BooleanField(default=False)  # Для модерации
    votes_to_approve = models.PositiveIntegerField(default=3)
    approved = models.BooleanField(default=False)

    likes = models.ManyToManyField(Account, related_name="liked_projects", blank=True)
    expert_likes = models.ManyToManyField(Account, related_name="expert_liked_projects", blank=True)

    duration = models.CharField(max_length=50, choices=[("semester", "1 семестр"), ("year", "1 год")],
                                default="semester")

    def check_approval(self):
        if self.expert_likes.count() >= 3:
            self.approved = True
            self.visible = True
            self.status = "open"
            self.save()

    def __str__(self):
        return self.title


class Idea(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('open', 'Опубликован'),
        ('under_review', 'На согласовании'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    technologies = models.ManyToManyField(Account, related_name="ideas_with", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ideas')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    visible = models.BooleanField(default=False)

    likes = models.ManyToManyField(Account, related_name="liked_ideas", blank=True)
    expert_likes = models.ManyToManyField(Account, related_name="experts_liked_ideas", blank=True)


# projects/models.py

class TeamResponse(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="team_responses")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="responses")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'team')  # чтобы нельзя было откликнуться дважды

