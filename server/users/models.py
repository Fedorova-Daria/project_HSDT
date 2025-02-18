from django.db import models
from core.models import Technology


class Account(models.Model):
    email = models.EmailField(unique=True)  # Почта

    first_name = models.CharField(max_length=100)  # Имя
    last_name = models.CharField(max_length=100)  # Фамилия
    phone = models.CharField(max_length=15)  # Телефон
    group = models.CharField(max_length=100)  # Группа в ВУЗе

    bio = models.TextField(blank=True, null=True)  # Био (необязательное)
    skills = models.ManyToManyField(Technology, related_name="users_with_skill", blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Аватарка (необязательное)

    total_rating = models.FloatField(default=0)  # Рейтинг
    rated_by_amount = models.FloatField(default=0)  # Рейтинг

    created_at = models.DateTimeField(auto_now_add=True)  # Дата регистрации

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


