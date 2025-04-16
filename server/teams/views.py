from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Team, TeamJoinRequest
from .serializers import (
    TeamListSerializer, TeamDetailSerializer, TeamEditSerializer,
    TeamCreateSerializer, JoinRequestSerializer
)
from users.models import Account
from projects.models import Project


class TeamListView(generics.ListAPIView):
    """Список всех команд с фильтрацией"""
    serializer_class = TeamListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Team.objects.all()
        # Фильтрация по статусу
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        # Фильтрация по технологии
        technology = self.request.query_params.get('technology')
        if technology:
            queryset = queryset.filter(members__skills__name=technology).distinct()
        return queryset


class TeamDetailView(generics.RetrieveAPIView):
    """Детальная информация о команде"""
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'team_id'  # Указываем, что параметр в URL называется team_id
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class TeamCreateView(generics.CreateAPIView):
    """Создание новой команды"""
    serializer_class = TeamCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Проверяем, что пользователь не состоит в другой команде
        if Team.objects.filter(members=self.request.user).exists():
            raise serializers.ValidationError("Вы уже состоите в другой команде")

        team = serializer.save(owner=self.request.user)
        team.members.add(self.request.user)  # Добавляем создателя в участники


class TeamUpdateView(generics.UpdateAPIView):
    """Редактирование команды (только для владельца)"""
    serializer_class = TeamEditSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'team_id'
    lookup_field = 'id'

    def get_queryset(self):
        return Team.objects.filter(owner=self.request.user)


class TeamMembersView(APIView):
    """Управление участниками команды"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, team_id):
        """Добавление участника по ID"""
        team = get_object_or_404(Team, id=team_id, owner=request.user)
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {'error': 'Не указан user_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Account.objects.get(id=user_id, role='ST')  # Только студенты
            if user in team.members.all():
                return Response(
                    {'error': 'Пользователь уже в команде'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            team.members.add(user)
            return Response(
                {'status': 'Участник добавлен'},
                status=status.HTTP_200_OK
            )
        except Account.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, team_id, user_id):
        """Удаление участника"""
        team = get_object_or_404(Team, id=team_id, owner=request.user)
        user = get_object_or_404(Account, id=user_id)

        if user == request.user:
            return Response(
                {'error': 'Вы не можете удалить себя из команды'},
                status=status.HTTP_400_BAD_REQUEST
            )

        team.members.remove(user)
        return Response(
            {'status': 'Участник удален'},
            status=status.HTTP_200_OK
        )


class TeamJoinView(APIView):
    """Запрос на вступление в команду"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, team_id):
        user = request.user
        team = get_object_or_404(Team, id=team_id)

        # Проверки
        if user in team.members.all():
            return Response(
                {'error': 'Вы уже в этой команде'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Team.objects.filter(members=user).exists():
            return Response(
                {'error': 'Вы уже состоите в другой команде'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if TeamJoinRequest.objects.filter(user=user, team=team).exists():
            return Response(
                {'error': 'Вы уже подавали заявку'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем заявку
        TeamJoinRequest.objects.create(
            user=user,
            team=team,
            message=request.data.get('message', '')
        )

        return Response(
            {'status': 'Заявка отправлена'},
            status=status.HTTP_201_CREATED
        )


class TeamRequestView(APIView):
    """Управление заявками на вступление"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, team_id, request_id, action):
        team = get_object_or_404(Team, id=team_id, owner=request.user)
        join_request = get_object_or_404(TeamJoinRequest, id=request_id, team=team)

        if action == 'accept':
            # Проверяем, что пользователь не в другой команде
            if Team.objects.filter(members=join_request.user).exists():
                join_request.status = 'declined'
                join_request.save()
                return Response(
                    {'error': 'Пользователь уже в другой команде'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            join_request.status = 'accepted'
            join_request.save()
            team.members.add(join_request.user)
            return Response({'status': 'Заявка принята'})

        elif action == 'reject':
            join_request.status = 'declined'
            join_request.save()
            return Response({'status': 'Заявка отклонена'})

        return Response(
            {'error': 'Неверное действие'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TeamLeaveView(APIView):
    """Выход из команды"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        user = request.user

        if user not in team.members.all():
            return Response(
                {'error': 'Вы не состоите в этой команде'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user == team.owner:
            return Response(
                {'error': 'Владелец не может покинуть команду'},
                status=status.HTTP_400_BAD_REQUEST
            )

        team.members.remove(user)
        return Response({'status': 'Вы вышли из команды'})


class TeamWithdrawRequestView(APIView):
    """Отзыв заявки на вступление"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, team_id):
        user = request.user
        team = get_object_or_404(Team, id=team_id)

        join_request = TeamJoinRequest.objects.filter(
            user=user,
            team=team,
            status='pending'
        ).first()

        if not join_request:
            return Response(
                {'error': 'Активная заявка не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        join_request.delete()
        return Response({'status': 'Заявка отозвана'})