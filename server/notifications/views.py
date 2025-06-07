from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from .models import Notification
from .serializers import NotificationSerializer
from .filters import NotificationFilter


class NotificationViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NotificationFilter

    def get_queryset(self):
        """
        Возвращает только уведомления текущего пользователя
        с поддержкой фильтрации по:
        - типу уведомления (type)
        - статусу прочтения (is_read)
        - связанной команде (related_team)
        - связанному проекту (related_project)
        - дате создания (created_after, created_before)
        """
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """
        Получение списка уведомлений с автоматической пометкой как прочитанные
        при запросе списка (если не указан параметр keep_unread=true)
        """
        queryset = self.filter_queryset(self.get_queryset())

# Не помечать как прочитанные, если есть параметр keep_unread
        if not request.query_params.get('keep_unread', '').lower() == 'true':
            # Обновляем только те, которые еще не прочитаны
            unread_notifications = queryset.filter(is_read=False)
            updated_count = unread_notifications.update(is_read=True)
            print(f"Updated {updated_count} notifications as read")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Получение количества непрочитанных уведомлений
        """
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Пометка конкретного уведомления как прочитанного
        """
        notification = self.get_object()
        if notification.user != request.user:
            return Response({'error': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)

        notification.is_read = True
        notification.save()
        return Response({'status': 'Уведомление помечено как прочитанное'})

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Пометка всех уведомлений пользователя как прочитанных
        """
        updated = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'status': f'{updated} уведомлений помечено как прочитанные'})