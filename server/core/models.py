from django.db import models



# Модель данных для списка технологий
from django.db import models

class Technology(models.Model):

    class TechCategory(models.TextChoices):
        PROGRAMMING = 'programming', 'Программирование'
        DESIGN = 'design', 'Дизайн'
        # можно добавить другие категории позже:
        # MANAGEMENT = 'management', 'Менеджмент'
        # MARKETING = 'marketing', 'Маркетинг'
        # и т.д.

    type = models.CharField(
        max_length=50,
        choices=TechCategory.choices,
        verbose_name="Раздел"
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название"
    )

    # users = models.ManyToManyField('users.Account' , related_name="technologies", verbose_name="Пользователи")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Технология"
        verbose_name_plural = "Технологии"



class UniversityGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)    # Создаём уникальное текстовое поле на 255 символов

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

