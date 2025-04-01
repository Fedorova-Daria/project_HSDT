from rest_framework import generics, permissions
from .models import Team
from .serializers import TeamDetailSerializer, TeamEditSerializer
from users.models import Account


class TeamListView(generics.ListAPIView):
    """Список всех команд"""
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamDetailView(generics.RetrieveAPIView):
    """Детальная информация о команде"""
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class TeamCreateView(generics.CreateAPIView):
    """Создание новой команды"""
    queryset = Team.objects.all()
    serializer_class = TeamEditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TeamUpdateView(generics.UpdateAPIView):
    """Редактирование команды (только для владельца)"""
    queryset = Team.objects.all()
    serializer_class = TeamEditSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Team.objects.filter(owner=self.request.user)


class TeamMembersView(generics.GenericAPIView):
    """Управление участниками команды"""
    queryset = Team.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        """Добавление участников"""
        team = self.get_object()
        if team.owner != request.user:
            return Response({'error': 'Только владелец может добавлять участников'},
                            status=status.HTTP_403_FORBIDDEN)

        user_ids = request.data.get('user_ids', [])
        # Добавьте логику добавления участников
        return Response({'status': 'success'})

    def delete(self, request, *args, **kwargs):
        """Удаление участников"""
        team = self.get_object()
        if team.owner != request.user:
            return Response({'error': 'Только владелец может удалять участников'},
                            status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        # Добавьте логику удаления участника
        return Response({'status': 'success'})