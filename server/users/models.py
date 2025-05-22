from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import Technology, UniversityGroup
from .managers import AccountManager
from django.contrib.auth import get_user_model
from django.conf import settings


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    phone = models.CharField(max_length=15, blank=True, null=True)  # Телефон
    university_group = models.ForeignKey(UniversityGroup, related_name='students', on_delete=models.CASCADE, null=True, blank=True)

    institute = models.CharField(max_length=100, blank=True, null=True)

    class Role(models.TextChoices):
        STUDENT = "ST", "Student"
        CUSTOMER = "CU", "Customer"
        EXPERT = "EX", "Expert"

    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.STUDENT
    )

    MODE_CHOICES = [
            ('light', 'Светлая'),
            ('dark', 'Тёмная'),
        ]

    mode = models.CharField(
        max_length=10,
        choices=MODE_CHOICES,
        default='light',
        verbose_name='Тема интерфейса'
    )

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    company_name = models.CharField(max_length=150, blank=True, null=True)

    bio = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField(Technology, related_name="users_with_skill", blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    total_rating = models.FloatField(default=0)
    rated_by_amount = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # Заполняем username email'ом
        super().save(*args, **kwargs)


class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey('teams.Team', on_delete=models.SET_NULL, null=True, blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.team or self.project} ({self.started_at})"

    @property
    def type(self):
        return "team" if self.team else "project"