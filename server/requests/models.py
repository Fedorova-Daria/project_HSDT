from django.db import models
from users.models import Account
from teams.models import Team
from datetime import timedelta
from django.utils.timezone import now

class TeamJoinRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидание"),
        ("accepted", "Принято"),
        ("rejected", "Отклонено"),
    ]

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="team_requests")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="join_requests")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        """Проверяем, истекла ли заявка (например, через 7 дней)"""
        return self.created_at < now() - timedelta(days=7)

    def __str__(self):
        return f"{self.user} -> {self.team} ({self.status})"

