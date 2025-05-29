from django.db import models
from django.contrib.auth import get_user_model
from teams.models import Team
from projects.models import Project

User = get_user_model()

class Board(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='boards')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Column(models.Model):
    COLUMN_TYPES = (
        ('default', 'Default'),
        ('completed', 'Completed'),
    )
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    column_type = models.CharField(max_length=20, choices=COLUMN_TYPES, default='default')

    class Meta:
        ordering = ['order']

class Task(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
