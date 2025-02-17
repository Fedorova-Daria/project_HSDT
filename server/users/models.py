from django.db import models


class Account(models.Model):
    email = models.EmailField(unique=True)  # Почта
    first_name = models.CharField(max_length=100)  # Имя
    last_name = models.CharField(max_length=100)  # Фамилия
    phone = models.CharField(max_length=15)  # Телефон
    group = models.CharField(max_length=100)  # Группа в ВУЗе
    bio = models.TextField(blank=True, null=True)  # Био (необязательное)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Аватарка (необязательное)
    team = models.CharField(max_length=100, blank=True, null=True)  # Команда (необязательное)
    rating = models.FloatField(default=0.0)  # Рейтинг

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

