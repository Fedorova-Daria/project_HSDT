from rest_framework.permissions import BasePermission

class IsTeamLeader(BasePermission):
    """
    Разрешение, позволяющее доступ только тимлиду (владельцу команды).
    """

    def has_permission(self, request, view):
        # Проверка только на уровне объекта
        return True

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

