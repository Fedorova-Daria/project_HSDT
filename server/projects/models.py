from django.db import models
from django.contrib.auth import get_user_model
from core.models import Technology
from users.models import Account


class Idea(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    initiator = models.ForeignKey(Account, related_name="ideas_initiated", on_delete=models.CASCADE, null=True)
    technologies = models.ManyToManyField(Technology, related_name="ideas")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Account, related_name='liked_ideas', blank=True)

    def __str__(self):
        return self.name


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