# core/perms.py
from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    """Разрешение только для студентов"""
    def has_permission(self, request, view):
        # Используем строковое сравнение роли вместо импорта модели
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'ST'


class IsCustomer(BasePermission):
    """Разрешение только для заказчика проекта"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Получаем проект из view (будет установлен в get_object)
        project = view.get_object()
        return project.customer == request.user