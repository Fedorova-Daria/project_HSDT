from django.db import models
from users.models import Account
from core.models import Technology

class Project(models.Model):
    votes_to_approve = 3

    STATUS_CHOICES = [
        ("draft", "Черновик"),  # Создан, но ещё не опубликован
        ("open", "Открыт"),  # Заказчика нет, можно предлагать себя
        ("customer_found", "Заказчик найден"),  # Есть заказчик, но исполнителей ещё нет
        ("in_progress", "В работе"),  # Работа над проектом идёт
        ("completed", "Завершён"),  # Всё готово
        ("cancelled", "Отменён"),  # Отменён по разным причинам
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    initiator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="initiated_projects")
    customer = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="client_projects")

    likes = models.ManyToManyField(Account, related_name="liked_projects", blank=True)  # Лайки проекта
    favorites = models.ManyToManyField(Account, related_name="favorite_projects", blank=True)  # Добавившие в избранное
    applicants = models.ManyToManyField(Account, related_name="applied_projects", blank=True)  # Откликнувшиеся на проект
    workers = models.ManyToManyField(Account, related_name="working_projects", blank=True)  # Выбранные заказчиком
    technologies = models.ManyToManyField(Technology, related_name="projects", blank=True)  # Технологии проекта

    # Статусы
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_hiring = models.BooleanField(default=True)  # Можно ли ещё записаться

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"


