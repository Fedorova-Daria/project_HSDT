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
    INSTITUTE_CHOICES = [
        ('HSDT', 'ВШЦТ'),
        ('IPTI', 'ИПТИ'),
        ('STROIN', 'СТРОИН'),
        ('ARHID', 'АРХИД'),
    ]
    
    name = models.CharField(max_length=255, unique=True)  # Уникальное текстовое поле на 255 символов
    institute = models.CharField(
        max_length=10, 
        choices=INSTITUTE_CHOICES,
        verbose_name="Институт",
        default='HSDT' 
    )

    def __str__(self):
        return f"{self.name} ({self.get_institute_display()})"

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        # Добавляем уникальность по комбинации имени и института
        unique_together = ['name', 'institute']


class Semester(models.Model):
    SEMESTER_CHOICES = [
        ('spring', 'Весенний'),
        ('winter', 'Зимний'),
    ]

    year = models.PositiveIntegerField()
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)

    class Meta:
        verbose_name = "Семестр"
        verbose_name_plural = "Семестры"
        unique_together = ('year', 'semester')
        ordering = ['-year', 'semester']

    def __str__(self):
        return f"{self.year} - {'Весенний' if self.semester == 'spring' else 'Зимний'} семестр"

