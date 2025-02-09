from django.db import models


class Team(models.Model):
    # Название команды (обязательное поле)
    name = models.CharField(max_length=100, unique=True)

    # Email участников (связь ManyToMany с UserProfile, так как участники - это пользователи)
    members = models.ManyToManyField('users.UserProfile', related_name='teams')

    # Максимальное количество участников
    max_members = models.IntegerField(default=5)  # По умолчанию 5 участников

    # Приватность команды (открытая или по приглашению)
    PRIVACY_CHOICES = [
        ('open', 'Открытая'),
        ('invite', 'По приглашению'),
    ]
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='open')

    # Описание команды
    description = models.TextField(blank=True, null=True)

    # Стек технологий
    technologies = models.ManyToManyField('technologies.Technology', related_name='teams')

    def __str__(self):
        return self.name

