# projects/views.py

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import status

from .serializers import (ProjectSerializer, ProjectUpdateSerializer, ProjectUpdateStatusSerializer,
                          IdeaSerializer, ProjectApplicationSerializer, IdeaEditSerializer)
from .permissions import IsStudent, IsOwnerOrReadOnly
from teams.models import Team
from .models import Idea, Project, ProjectApplication


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectUpdateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProjectUpdateSerializer
        return ProjectSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy',
                           'like', 'favorite', 'apply', 'vote']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create']:
            return [IsStudent()]
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

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return IdeaEditSerializer
        return IdeaSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticatedOrReadOnly(), IsStudent()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticatedOrReadOnly(), IsOwnerOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Idea.objects.all()
        return Idea.objects.filter(visible=True, status='open')

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
    permission_classes = [permissions.IsAuthenticated]  # можно кастомизировать

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        if data['applicant_type'] == 'freelancer':
            serializer.save(freelancer=user)
        elif data['applicant_type'] == 'team':
            # тут можно проверить, владеет ли юзер этой командой
            serializer.save()

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        app = self.get_object()
        project = app.project

        if project.owner != request.user:
            return Response({'detail': 'Нет доступа'}, status=403)

        if app.status != 'pending':
            return Response({'detail': 'Заявка уже обработана'}, status=400)

        # Обработка по типу заявки
        if app.applicant_type == 'freelancer' and app.freelancer:
            if app.freelancer in project.workers.all():
                return Response({'detail': 'Фрилансер уже в проекте'}, status=400)
            project.workers.add(app.freelancer)

        elif app.applicant_type == 'team' and app.team:
            if app.team in project.teams.all():
                return Response({'detail': 'Команда уже в проекте'}, status=400)
            project.teams.add(app.team)

        else:
            return Response({'detail': 'Тип заявки или данные некорректны'}, status=400)

        app.status = 'accepted'
        app.save()
        project.save()

        return Response({'status': 'accepted'})

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        app = self.get_object()
        if app.project.owner != request.user:
            return Response({'detail': 'Нет доступа'}, status=403)
        app.status = 'rejected'
        app.save()
        return Response({'status': 'rejected'})

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

