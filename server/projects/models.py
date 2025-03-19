from django.db import models
from django.contrib.auth import get_user_model
from core.models import Technology
from users.models import Account


class Idea(models.Model):
    votes_to_approve = 1

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    short_description = models.TextField(blank=True)
    initiator = models.ForeignKey(Account, related_name="ideas_initiated", on_delete=models.CASCADE, null=True)
    experts_voted = models.ManyToManyField(Account, related_name="voted_for", blank=True)
    technologies = models.ManyToManyField(Technology, related_name="ideas", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Account, related_name='liked_ideas', blank=True)

    @property
    def approved(self):
        return self.experts_voted.count() >= self.votes_to_approve

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Идея"
        verbose_name_plural = "Идеи"


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    owner = models.ForeignKey(Account, related_name="teams_owned", on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(Account, related_name="teams")

    is_private = models.BooleanField(default=True)
    max_members = models.PositiveSmallIntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    customer = models.CharField(max_length=255, unique=True)
    initiator = models.ForeignKey(Account, related_name="projects_initiated", on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(Team, related_name="projects_initiated", on_delete=models.CASCADE, null=True)

    technologies = models.ManyToManyField(Technology, related_name="projects")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name