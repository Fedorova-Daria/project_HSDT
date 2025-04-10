from rest_framework import generics, permissions
from .models import Team
from .serializers import TeamDetailSerializer, TeamEditSerializer, TeamJoinRequestSerializer
from users.models import Account
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Team, TeamJoinRequest


class TeamJoinRequestListView(generics.ListAPIView):
    queryset = TeamJoinRequest.objects.all()
    serializer_class = TeamJoinRequestSerializer


class TeamJoinRequestDetailView(generics.ListAPIView):
    queryset = TeamJoinRequest.objects.all()
    serializer_class = TeamJoinRequestSerializer
    lookup_field = 'id'


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
        team.members.add(self.request.user)  # Добавляем создателя в участники. Да, я добавил только одну строчку и что?


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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_team(request, team_id):
    user = request.user

    if user.teams.exists():
        return Response({"detail": "Вы уже состоите в команде."}, status=400)

    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response({"detail": "Команда не найдена."}, status=404)

    if TeamJoinRequest.objects.filter(user=user, team=team).exists():
        return Response({"detail": "Вы уже отправили заявку."}, status=400)

    TeamJoinRequest.objects.create(user=user, team=team)
    return Response({"detail": "Заявка отправлена."}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request(request, team_id, request_id):
    user = request.user

    try:
        team = Team.objects.get(id=team_id)
        join_request = TeamJoinRequest.objects.get(id=request_id, team=team)
    except (Team.DoesNotExist, TeamJoinRequest.DoesNotExist):
        return Response({"detail": "Команда или заявка не найдена."}, status=404)

    if team.owner != user:
        return Response({"detail": "Вы не владелец команды."}, status=403)

    join_request.status = 'accepted'
    join_request.save()
    team.members.add(join_request.user)

    return Response({"detail": "Заявка принята."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deny_request(request, team_id, request_id):
    user = request.user

    try:
        team = Team.objects.get(id=team_id)
        join_request = TeamJoinRequest.objects.get(id=request_id, team=team)
    except (Team.DoesNotExist, TeamJoinRequest.DoesNotExist):
        return Response({"detail": "Команда или заявка не найдена."}, status=404)

    if team.owner != user:
        return Response({"detail": "Вы не владелец команды."}, status=403)

    join_request.status = 'declined'
    join_request.save()

    return Response({"detail": "Заявка отклонена."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_team(request, team_id):
    user = request.user

    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response({"detail": "Команда не найдена."}, status=404)

    if user not in team.members.all():
        return Response({"detail": "Вы не состоите в команде."}, status=400)

    team.members.remove(user)
    return Response({"detail": "Вы покинули команду."})

