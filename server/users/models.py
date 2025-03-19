from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import Technology, UniversityGroup
from .managers import AccountManager
from django.contrib.auth import get_user_model


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    phone = models.CharField(max_length=15, blank=True, null=True)  # Телефон
    university_group = models.ForeignKey(UniversityGroup, related_name='students', on_delete=models.CASCADE, null=True, blank=True)

    class Role(models.TextChoices):
        STUDENT = "ST", "Student"
        CUSTOMER = "CU", "Customer"
        EXPERT = "EX", "Expert"

    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.STUDENT
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

