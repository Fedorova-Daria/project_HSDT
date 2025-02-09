from django.db import models

from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Название технологии (Vue.js, Django и т. д.)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Technologies'  # Исправляем множественное число

