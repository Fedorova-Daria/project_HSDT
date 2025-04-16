# projects/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, TeamResponse
from .serializers import ProjectSerializer, ProjectCreateSerializer, ProjectUpdateStatusSerializer
from django.shortcuts import get_object_or_404

from .models import Idea
from .serializers import IdeaSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsStudent, IsOwnerOrReadOnly

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from teams.models import Team


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProjectUpdateStatusSerializer
        return ProjectSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy',
                           'like', 'favorite', 'apply', 'vote']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

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
    def favorite(self, request, pk=None):
        project = self.get_object()
        user = request.user
        if user in project.favorites.all():
            project.favorites.remove(user)
            return Response({'detail': 'Убрано из избранного'})
        project.favorites.add(user)
        return Response({'detail': 'Добавлено в избранное'})

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        project = self.get_object()
        user = request.user
        if user in project.applicants.all():
            return Response({'detail': 'Вы уже откликнулись'}, status=status.HTTP_400_BAD_REQUEST)
        project.applicants.add(user)
        return Response({'detail': 'Отклик принят'})

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        project = self.get_object()
        user = request.user
        if user in project.experts_voted.all():
            return Response({'detail': 'Вы уже голосовали'}, status=status.HTTP_400_BAD_REQUEST)
        project.experts_voted.add(user)
        if project.experts_voted.count() >= project.votes_to_approve:
            project.approved = True
            project.visible = True
            project.status = "open"
            project.save()
        return Response({'detail': 'Голос учтён'})


class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer

    def get_permissions(self):
        if self.action == 'create_idea':
            return [IsAuthenticatedOrReadOnly(), IsStudent()]
        elif self.action in ['edit_idea']:
            return [IsAuthenticatedOrReadOnly(), IsOwnerOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Idea.objects.all()
        return Idea.objects.filter(visible=True, status='open')

    @action(detail=False, methods=['post'], url_path='create')
    def create_idea(self, request):
        serializer = IdeaEditSerializer(idea, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'], url_path='edit')
    def edit_idea(self, request, pk=None):
        idea = self.get_object()
        self.check_object_permissions(request, idea)
        serializer = IdeaEditSerializer(idea, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        idea = self.get_object()
        user = request.user

        if user in idea.likes.all():
            idea.likes.remove(user)
            liked = False
        else:
            idea.likes.add(user)
            liked = True

        return Response({'liked': liked, 'likes_count': idea.likes.count()})


class TeamRespondToProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        user = request.user
        try:
            team = user.owned_team  # получаем команду, где он тим-лид
        except Team.DoesNotExist:
            return Response({"detail": "Вы не являетесь тим-лидом ни одной команды."}, status=400)

        project = get_object_or_404(Project, id=project_id)

        if project.selected_team:
            return Response({"detail": "Команда уже выбрана."}, status=400)

        if project.status in ["in_progress", "done"]:
            return Response({"detail": "Нельзя откликнуться на завершённый или выполняемый проект."}, status=400)

        response, created = TeamResponse.objects.get_or_create(project=project, team=team)

        if not created:
            return Response({"detail": "Вы уже откликались на этот проект."}, status=400)

        return Response({"detail": "Команда успешно откликнулась на проект."})


class SelectTeamForProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, team_id):
        project = get_object_or_404(Project, id=project_id)

        if project.owner != request.user:
            return Response({"detail": "Только заказчик может выбрать команду."}, status=403)

        team = get_object_or_404(Team, id=team_id)

        if not TeamResponse.objects.filter(project=project, team=team).exists():
            return Response({"detail": "Эта команда не откликалась на проект."}, status=400)

        project.selected_team = team
        project.status = "in_progress"
        project.save()

        return Response({"detail": f"Команда '{team.name}' выбрана для реализации проекта."})

