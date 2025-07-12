# projects/views.py

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from collections import defaultdict

from .serializers import (ProjectSerializer, ProjectUpdateSerializer, ProjectUpdateStatusSerializer, ProjectMessageSerializer,
                        IdeaSerializer, ProjectApplicationSerializer, IdeaEditSerializer, ProjectParticipantRatingSerializer, ProjectParticipantDetailSerializer)
from .permissions import IsStudent, IsOwnerOrReadOnly
from teams.models import Team
from .models import Idea, Project, ProjectApplication, ProjectParticipantRating, ProjectMessage
from .filters import ProjectFilter, IdeaFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProjectFilter
from users.models import Account
from kanban.models import Board, Column

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter


    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectUpdateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProjectUpdateSerializer
        return ProjectSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'like', 'favorite', 'apply', 'expert_like']:
            # Требуем авторизацию для определенных действий
            return [IsAuthenticated()]
        # Для всех остальных действий доступ разрешен всем (включая неавторизованных пользователей)
        return [AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(initiator=user, owner=user)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            return Response({'detail': 'Вы не являетесь владельцем проекта'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        project = self.get_object()
        user = request.user
        if user in project.likes.all():
            project.likes.remove(user)
            return Response({'detail': 'Убрано из лайков'})
        project.likes.add(user)
        return Response({'detail': 'Добавлено в лайки'})

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        project = self.get_object()
        user = request.user
        if user in project.applicants.all():
            return Response({'detail': 'Вы уже откликнулись'}, status=status.HTTP_400_BAD_REQUEST)
        project.applicants.add(user)
        return Response({'detail': 'Отклик принят'})

    @action(detail=True, methods=['post'])
    def expert_like(self, request, pk=None):
        project = self.get_object()
        user = request.user

        # Проверка: уже лайкнул?
        if user in project.expert_likes.all():
            project.expert_likes.remove(user)
            return Response({'detail': 'Лайк эксперта убран'})

        project.expert_likes.add(user)
        project.check_approval()

        return Response({'detail': 'Лайк эксперта добавлен'})
    
    @action(detail=True, methods=['post'])
    def send_for_revision(self, request, pk=None):
        project = self.get_object()
        text = request.data.get('text')
        is_revision = request.data.get('is_revision_request', False)
        sender_role = request.data.get('sender_role', 'admin')

        if not text:
            return Response({'error': 'Text is required'}, status=400)
        project.status = 'under_revision'
        project.save()

        msg = ProjectMessage.objects.create(
            project=project,
            sender=request.user,
            text=text,
            is_revision_request=is_revision,
            sender_role=sender_role
        )

        return Response({'detail': 'Project sent for revision', 'message_id': msg.id}, status=200)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        project = self.get_object()
        messages = ProjectMessage.objects.filter(project=project).order_by('-created_at')
        serializer = ProjectMessageSerializer(messages, many=True)
        return Response(serializer.data)

        return Response({'status': 'revision_requested'})

    @action(detail=True, methods=['post'])
    def confirm_changes(self, request, pk=None):
        project = self.get_object()

        # Найти последнее сообщение с флагом is_revision_request=True
        last_msg = project.messages.filter(is_revision_request=True).order_by('-created_at').first()

        if not last_msg:
            return Response({'error': 'No revision request found'}, status=400)

        # Проверяем роль, чтобы определить новый статус
        if last_msg.sender_role == 'admin':
            project.status = 'new'
        elif last_msg.sender_role == 'expert':
            project.status = 'review'
        else:
            return Response({'error': 'Unknown sender role'}, status=400)

        project.save()
        return Response({'detail': 'Project status updated successfully'}, status=200)

    @action(detail=False, methods=["get"])
    def grouped_by_semester(self, request):
        # Используй filterset_class, передавая туда request.GET и queryset
        filtered_qs = self.filterset_class(request.GET, queryset=self.get_queryset()).qs

        # Здесь дополнительный фильтр по видимости (если нужен)
        visible_param = request.query_params.get("visible")
        if visible_param is not None:
            if visible_param.lower() == "true":
                filtered_qs = filtered_qs.filter(visible=True)
            elif visible_param.lower() == "false":
                filtered_qs = filtered_qs.filter(visible=False)

        # Оптимизируем запрос
        projects = filtered_qs.select_related("semester").order_by('-semester__year', 'semester__semester')

        grouped = defaultdict(lambda: {'spring': [], 'winter': []})

        for project in projects:
            if project.semester:
                year = project.semester.year
                sem = project.semester.semester  # 'spring' или 'winter'
                grouped[year][sem].append(ProjectSerializer(project).data)

        result = []
        for year in sorted(grouped.keys(), reverse=True):
            result.append({
                "year": year,
                "spring": grouped[year]["spring"],
                "winter": grouped[year]["winter"]
            })

        return Response(result)

class ProjectParticipantRatingViewSet(viewsets.ModelViewSet):
    queryset = ProjectParticipantRating.objects.all()
    serializer_class = ProjectParticipantRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(rated_by=self.request.user)


class ProjectParticipantsDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'detail': 'Проект не найден'}, status=404)

        serializer = ProjectParticipantDetailSerializer(project)
        return Response(serializer.data)

class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = IdeaFilter

    def create_private_idea(owner, team, title, description, skills=None):
        """Создает идею, привязанную к приватной команде."""
        if not team.can_create_idea():
            raise TeamNotPrivateError("Только приватные команды могут создавать идеи.")

        idea = Idea.objects.create(
            owner=owner,
            team=team,
            title=title,
            description=description,
            status="private"
        )
        if skills:
            idea.skills_required.set(skills)

        # Создание канбан-доски для новой идеи
        board = Board.objects.create(
            team=team,
            idea=idea,
            project=None  # Для идей проект не указываем
        )
        
        # Создание базовых колонок для доски идеи
        create_default_columns(board)

        return idea

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return IdeaEditSerializer
        return IdeaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Idea.objects.all()
        return Idea.objects.filter(visible=True, status='open')

    def perform_create(self, serializer):
        # 👇 вот это добавь
        serializer.save(owner=self.request.user)


    @action(detail=True, methods=['post'], url_path='like', permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        idea = self.get_object()
        user = request.user

        if user in idea.likes.all():
            idea.likes.remove(user)
            liked = False
        else:
            idea.likes.add(user)
            liked = True

        return Response({
            'liked': liked,
            'likes_count': idea.likes.count(),
        })



class ProjectApplicationViewSet(viewsets.ModelViewSet):
    queryset = ProjectApplication.objects.all()
    serializer_class = ProjectApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        if data['applicant_type'] == 'freelancer':
            serializer.save(freelancer=user)
        elif data['applicant_type'] == 'team':
            serializer.save()
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        app = self.get_object()
        project = app.project

        if app.status != 'pending':
            return Response({'detail': 'Заявка уже обработана'}, status=status.HTTP_400_BAD_REQUEST)

        if app.applicant_type == 'freelancer' and app.freelancer:
            if app.freelancer in project.workers.all():
                return Response({'detail': 'Фрилансер уже в проекте'}, status=status.HTTP_400_BAD_REQUEST)
            project.workers.add(app.freelancer)

        elif app.applicant_type == 'team' and app.team:
            if app.team in project.teams.all():
                return Response({'detail': 'Команда уже в проекте'}, status=status.HTTP_400_BAD_REQUEST)
            project.teams.add(app.team)

            # Создание канбан-доски для команды, которая была добавлена в проект
            board = Board.objects.create(
                team=app.team,
                project=project
            )

            self.create_default_columns(board)

        else:
            return Response({'detail': 'Тип заявки или данные некорректны'}, status=status.HTTP_400_BAD_REQUEST)

        app.status = 'accepted'
        app.save()
        project.save()

        return Response({'status': 'accepted'})

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        app = self.get_object()
        #if app.project.owner != request.user:
        #    return Response({'detail': 'Нет доступа'}, status=403)
        app.status = 'rejected'
        app.save()
        return Response({'status': 'rejected'})
    # Можно добавить уведомление об отклонении, если нужно

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        app = self.get_object()
        user = request.user
        is_freelancer = app.freelancer == user
        is_team_owner = app.team and app.team.owner == user
        if not is_freelancer and not is_team_owner:
            return Response({'detail': 'Нет доступа'}, status=403)
        app.status = 'cancelled'
        app.save()
        return Response({'status': 'cancelled'})
    

@api_view(['POST'])
def add_project_to_team(request, team_id, project_id):
    try:
        # Получаем команду и проект
        team = Team.objects.get(id=team_id)
        project = Project.objects.get(id=project_id)
        
        # Добавляем проект к команде
        team.projects.add(project)
        team.save()

        return Response({'message': 'Проект успешно добавлен к команде'}, status=status.HTTP_200_OK)
    except Team.DoesNotExist:
        return Response({'error': 'Команда не найдена'}, status=status.HTTP_404_NOT_FOUND)
    except Project.DoesNotExist:
        return Response({'error': 'Проект не найден'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def add_idea_to_team(request, team_id, idea_id):
    try:
        team = Team.objects.get(id=team_id)
        idea = Idea.objects.get(id=idea_id)

        # Добавляем идею к команде
        team.ideas.add(idea)
        team.save()

        return Response({'message': 'Идея успешно добавлена к команде'}, status=status.HTTP_200_OK)

    except Team.DoesNotExist:
        return Response({'error': 'Команда не найдена'}, status=status.HTTP_404_NOT_FOUND)
    except Idea.DoesNotExist:
        return Response({'error': 'Идея не найдена'}, status=status.HTTP_404_NOT_FOUND)


def create_default_columns(self, board):
    """Создание базовых колонок для новой доски"""
    default_columns = [
        {'title': 'Сделать', 'column_type': 'default', 'order': 1},
        {'title': 'В процессе', 'column_type': 'default', 'order': 2},
        {'title': 'Готово','column_type': 'completed', 'order': 3}
    ]
    for col_data in default_columns:
        Column.objects.create(board=board, **col_data)