from django.db import models


# Модель данных для списка технологий
class Technology(models.Model):
    name = models.CharField(max_length=255, unique=True)    # Создаём уникальное текстовое поле на 255 символов

    def __str__(self):
        return self.name

    # Залезаем в класс "метаданных", который мы унаследовали из Model
    class Meta:
        verbose_name = "Технология"
        verbose_name_plural = "Технологии"


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)    # Создаём уникальное текстовое поле на 255 символов

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

