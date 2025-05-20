from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsTeamLeader
from rest_framework.permissions import IsAuthenticated
from .models import Team, TeamJoinRequest
from .serializers import (
    TeamCreateSerializer,
    TeamListSerializer,
    TeamDetailSerializer,
    TeamUpdateSerializer,
    TeamJoinRequestSerializer
)
from .filters import TeamJoinRequestFilter, TeamFilter
from notifications.utils import *
from django_filters.rest_framework import DjangoFilterBackend


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeamFilter

    def get_serializer_class(self):
        if self.action == "create":
            return TeamCreateSerializer
        if self.action == "list":
            return TeamListSerializer
        if self.action == "retrieve":
            return TeamDetailSerializer
        if self.action in ["update", "partial_update"]:
            return TeamUpdateSerializer
        return TeamDetailSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_update(self, serializer):
        team = self.get_object()
        if self.request.user != team.owner:
            raise PermissionError("Только тим-лид может редактировать команду.")
        serializer.save()

    @action(detail=True, methods=["post"], permission_classes=[IsTeamLeader])
    def add_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get("user_id")

        try:
            user = Account.objects.get(id=user_id)
        except Account.DoesNotExist:
            return Response({"detail": "Пользователь не найден."}, status=404)

        if user.teams.exists():
            return Response({"detail": "Пользователь уже в команде."}, status=400)

        team.members.add(user)

        # Отклоняем заявки во все команды
        TeamJoinRequest.objects.filter(user=user, status='pending').update(status='declined')

        return Response({"detail": "Пользователь добавлен в команду."})

    @action(detail=True, methods=["post"], permission_classes=[IsTeamLeader])
    def remove_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"detail": "Не указан ID пользователя."}, status=400)

        try:
            user = Account.objects.get(id=user_id)
        except Account.DoesNotExist:
            return Response({"detail": "Пользователь не найден."}, status=404)

        if user == team.owner:
            return Response({"detail": "Нельзя удалить тимлида."}, status=400)

        if user not in team.members.all():
            return Response({"detail": "Пользователь не состоит в команде."}, status=400)

        team.members.remove(user)

        return Response({"detail": "Пользователь удалён из команды."})


class TeamJoinRequestViewSet(viewsets.ModelViewSet):
    queryset = TeamJoinRequest.objects.all().order_by('-created_at')
    serializer_class = TeamJoinRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeamJoinRequestFilter


    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TeamJoinRequest.objects.all()
        return TeamJoinRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        join_request = self.get_object()
        if join_request.user != request.user:
            return Response({"detail": "Нельзя удалить чужую заявку."}, status=403)
        if join_request.status != 'pending':
            return Response({"detail": "Нельзя отменить обработанную заявку."}, status=400)

        join_request.delete()
        return Response({"detail": "Заявка отозвана."})

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        join_request = self.get_object()
        team = join_request.team

        if team.owner != request.user:
            return Response({"detail": "Только тимлид может принимать заявки."}, status=403)

        if join_request.user.teams.exists():
            return Response({"detail": "Пользователь уже состоит в команде."}, status=400)

        join_request.status = 'accepted'
        join_request.save()

        team.members.add(join_request.user)

        TeamJoinRequest.objects.filter(
            user=join_request.user,
            status='pending'
        ).exclude(id=join_request.id).update(status='declined')

        notify_team_join_accepted(request.user, team, join_request)

        return Response({"detail": "Участник добавлен в команду."})

    @action(detail=True, methods=["post"])
    def decline(self, request, pk=None):
        join_request = self.get_object()
        if join_request.team.owner != request.user:
            return Response({"detail": "Нет прав."}, status=403)

        join_request.status = 'declined'
        join_request.save()
        return Response({"detail": "Заявка отклонена."})

