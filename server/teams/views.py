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
from users.models import Account
from .filters import TeamJoinRequestFilter, TeamFilter
from notifications.utils import *
from django_filters.rest_framework import DjangoFilterBackend
from kanban.models import Board
from projects.models import Project
from django.utils import timezone
from users.models import UserActivity


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
    
    def perform_create(self, serializer):
        team = serializer.save()

        board = Board.objects.create(
            team=team,
            project=None
        )

        return team

    def perform_update(self, serializer):
        team = self.get_object()
        if self.request.user != team.owner:
            raise PermissionError("Только тим-лид может редактировать команду.")
        serializer.save()

    @action(detail=True, methods=['get'])
    def board_options(self, request, pk=None): # !!!
        team = self.get_object()
        
        # Получаем проекты со статусом 'in_process'
        projects_in_process = Project.objects.filter(
            id__in=team.projects.all(),
            status='in_progress'
        ).values('id', 'title', 'description')
        print(projects_in_process)  # Выводим полученные проекты в консоль
        # Получаем идеи (если нужно)
        ideas = team.ideas.all().values('id', 'title', 'description')
        
        return Response({
            'projects': list(projects_in_process),
            'ideas': list(ideas)
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated]) # !!!
    def disband(self, request, pk=None):
        """Распад команды с сохранением связей для статистики"""
        team = self.get_object()
        user = request.user
        
        # Проверяем права доступа
        if team.owner != user:
            return Response({
                'detail': 'Только владелец команды может распустить команду'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Проверяем текущий статус
        if team.status == 'over':
            return Response({
                'detail': 'Команда уже распущена',
                'disbanded_at': team.disbanded_at
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Сохраняем информацию для уведомлений
            members_to_notify = list(team.members.all())
            boards_count = self._count_team_boards(team)
            projects_count = team.projects.count()
            ideas_count = team.ideas.count()
            
            # Выполняем распад команды
            disbanded_data = self._disband_team_internal(team)
            
            # Отправляем уведомления
            self._notify_team_disbandment(team, members_to_notify)
            
            return Response({
                'detail': 'Команда успешно распущена',
                'team_id': team.id,
                'status': team.status,
                'disbanded_at': team.disbanded_at,
                'removed_members_count': len(members_to_notify),
                'deleted_boards_count': disbanded_data['deleted_boards'],
                'preserved_projects_count': projects_count,
                'preserved_ideas_count': ideas_count,
                'note': 'Связи с проектами и идеями сохранены для статистики'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'detail': 'Ошибка при распуске команды',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _disband_team_internal(self, team):
        """Внутренний метод для распуска команды"""
        disbanded_data = {
            'deleted_boards': 0
        }

        # Закрываем активность участников
        self._close_team_members_activity(team)

        # 1. Удаляем все канбан доски команды
        deleted_boards = self._delete_team_boards(team)
        disbanded_data['deleted_boards'] = deleted_boards
        
        # 2. Очищаем участников команды
        team.members.clear()
        
        # 3. Изменяем статус и заполняем disbanded_at
        team.status = 'over'
        team.disbanded_at = timezone.now()
        
        # 4. Сохраняем изменения
        team.save()
        
        print(f"Команда {team.id} распущена. Связи с проектами и идеями сохранены.")
        
        return disbanded_data
    
    def _close_team_members_activity(self, team):
        """Закрытие активности всех участников команды при распаде"""
        from users.models import UserActivity  # Правильный импорт
        
        disbandment_time = timezone.now()
        closed_activities_count = 0
        
        # Получаем все активные записи UserActivity для данной команды
        active_activities = UserActivity.objects.filter(
            team=team,
            ended_at__isnull=True
        )
        
        for activity in active_activities:
            activity.ended_at = disbandment_time
            activity.save()
            closed_activities_count += 1
            print(f"Закрыта активность пользователя {activity.user.id} в команде {team.id}")
        
        print(f"Закрыто {closed_activities_count} активных записей при распаде команды {team.id}")

        return closed_activities_count

    def _delete_team_boards(self, team):
        """Удаление всех канбан досок команды"""
        try:
            from kanban.models import Board, Column, Task  # Правильный импорт
            
            boards = Board.objects.filter(team=team)
            deleted_count = 0
            
            for board in boards:
                # Удаляем все задачи в колонках доски
                columns = Column.objects.filter(board=board)
                for column in columns:
                    Task.objects.filter(column=column).delete()
                
                # Удаляем все колонки доски
                columns.delete()
                
                # Удаляем саму доску
                board.delete()
                deleted_count += 1
                
                print(f"Удалена доска ID: {board.id} команды {team.id}")
            
            return deleted_count
            
        except ImportError:
            print("Модули kanban не найдены, пропускаем удаление досок")
            return 0

    def _count_team_boards(self, team):
        """Подсчет количества досок команды"""
        try:
            from kanban.models import Board  # Правильный импорт
            return Board.objects.filter(team=team).count()
        except ImportError:
            print("Модуль kanban.models не найден")
            return 0

    def _notify_team_disbandment(self, team, members):
        """Отправка уведомлений о распуске команды"""
        for member in members:
            try:
                # Если у вас есть система уведомлений, раскомментируйте:
                # from notifications.models import Notification
                # Notification.objects.create(
                #     user=member,
                #     title=f'Команда "{team.name}" распущена',
                #     message=f'Команда "{team.name}" была распущена владельцем. '
                #             f'История участия в проектах и идеях сохранена.',
                #     notification_type='team_disbanded',
                #     related_team=team
                # )
                print(f"Уведомление отправлено пользователю {member.id} о распуске команды {team.id}")
            except Exception as e:
                print(f"Ошибка отправки уведомления пользователю {member.id}: {e}")

                
    @action(detail=True, methods=["post"], permission_classes=[IsTeamLeader])
    def add_member(self, request, pk=None):
        team = self.get_object() 
        user_id = request.data.get("user_id") 
        if not user_id:
            return Response({"detail": "Не указан ID пользователя."}, status=400)

        try:
            user = Account.objects.get(id=user_id)
        except Account.DoesNotExist:
            return Response({"detail": "Пользователь не найден."}, status=404)

        if team.members.filter(id=user.id).exists():
            return Response({"detail": "Пользователь уже в команде."}, status=400)

        if user.teams.exists():
            return Response({"detail": "Пользователь уже состоит в другой команде."}, status=400)

        team.members.add(user)

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
        user = self.request.user
        team = serializer.validated_data.get('team')

        if TeamJoinRequest.objects.filter(user=user, team=team).exists():
            raise ValueError("Заявка от этого пользователя уже существует для этой команды.")
        
        team_join_request = serializer.save(user=user)

        create_notification(
            user=team.owner, 
            notification_type='team_join_request_sent',
            message=f"{user.get_full_name()} подал(а) заявку на присоединение к вашей команде {team.name}.",
            related_team=team,
            related_team_join_request=team_join_request,
            is_read=False  
        )

        serializer.save(user=user)

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

        return Response({"detail": "Участник добавлен в команду."})

    @action(detail=True, methods=["post"])
    def decline(self, request, pk=None):
        join_request = self.get_object()
        if join_request.team.owner != request.user:
            return Response({"detail": "Нет прав."}, status=403)

        join_request.status = 'declined'
        join_request.save()
        return Response({"detail": "Заявка отклонена."})