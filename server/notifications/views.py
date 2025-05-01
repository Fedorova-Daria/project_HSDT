from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]  # Проверка через JWT и сессии
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Возвращаем уведомления только для текущего пользователя
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
