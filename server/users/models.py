from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, group, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, group=group)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, group, password=None):
        user = self.create_user(email, first_name, last_name, group, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    email = models.EmailField(unique=True)  # Почта как уникальный идентификатор
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    group = models.CharField(max_length=100)  # Группа в вузе
    technologies = models.ManyToManyField('technologies.Technology', blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Задаём, что юзернеймом будет почта
    REQUIRED_FIELDS = ['first_name', 'last_name', 'group']  # Обязательные поля для создания суперпользователя

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

