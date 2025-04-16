from django.db import models
from django.conf import settings
from core.models import Technology  # если технологии из core
from teams.models import Team  # если используем команды

User = settings.AUTH_USER_MODEL


class Idea(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('open', 'Опубликован'),
        ('under_review', 'На согласовании'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ideas')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    visible = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    likes = models.ManyToManyField(Account, related_name="liked_ideas", blank=True)
    expert_likes = models.ManyToManyField(Account, related_name="expert_liked_projects", blank=True)

    def check_approval(self):
        if self.expert_likes.count() >= 3:
            self.approved = True
            self.visible = True
            self.status = "open"
            self.save()

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
    skills_required = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='projects_owned')
    initiator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='projects_initiated')
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='projects_customer')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    visible = models.BooleanField(default=False)  # Для модерации
    votes_to_approve = models.PositiveIntegerField(default=0)
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


class ProjectRequest(models.Model):
    """
    Запрос от студента или команды на участие в проекте.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    message = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=[
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"Request: {self.user} -> {self.project}"

