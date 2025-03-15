from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """Разрешение только для пользователей с ролью 'Заказчик'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Заказчик").exists()


class IsStudent(BasePermission):
    """Разрешение только для пользователей с ролью 'Студент'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Студент").exists()


class IsExpert(BasePermission):
    """Разрешение только для пользователей с ролью 'Эксперт'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Эксперт").exists()

