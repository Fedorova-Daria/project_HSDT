from django.db import models
from users.models import Account


class Team(models.Model):
    STATUS_CHOICES = [
        ("open", "Открыта"),
        ("private", "Приватная"),
        ("disbanded", "Расформирована"),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    owner = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="owned_team")
    members = models.ManyToManyField(Account, related_name="teams", blank=True)
    avatar = models.ImageField(upload_to="team_avatars/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")

    def __str__(self):
        return self.name

