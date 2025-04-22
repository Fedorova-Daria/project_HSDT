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
    initiator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='projects_initiated', blank=True, null=True)

    teams = models.ManyToManyField(Account, related_name='teams_projects', blank=True, null=True)
    workers = models.ManyToManyField(Account, related_name='workers_projects', blank=True, null=True)

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
    skills_required = models.ManyToManyField(Technology, related_name="ideas_with", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ideas')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    visible = models.BooleanField(default=False)

    likes = models.ManyToManyField(Account, related_name="liked_ideas", blank=True)
    expert_likes = models.ManyToManyField(Account, related_name="experts_liked_ideas", blank=True)

    def __str__(self):
        return self.title


# projects/models.py

class ProjectApplication(models.Model):
    APPLICANT_TYPE_CHOICES = (
        ('freelancer', 'Фрилансер'),
        ('team', 'Команда'),
    )

    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('cancelled', 'Отменено'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    applicant_type = models.CharField(max_length=20, choices=APPLICANT_TYPE_CHOICES)
    freelancer = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
