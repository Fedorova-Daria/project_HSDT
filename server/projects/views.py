from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers, viewsets, permissions, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectListSerializer, ProjectCreateSerializer
from users.models import Account
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404


class ProjectListView(generics.ListAPIView):
    """
    API endpoint для отображения списка всех проектов.
    Использует ProjectListSerializer для сериализации данных.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    def get_serializer_context(self):
        # Передаем request в контекст сериализатора для проверки is_liked
        return {'request': self.request}


class ProjectLikeView(APIView):
    """
    API endpoint для добавления/удаления лайков проектов.
    - Только для авторизованных пользователей
    - Добавляет пользователя в likes при запросе
    - Удаляет лайк если пользователь уже лайкнул
    - Для экспертов также добавляет/удаляет голос в experts_voted
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            user = request.user
            response_data = {
                'status': 'success',
                'likes_count': project.likes.count(),
                'experts_voted_count': project.experts_voted.count(),
                'user_role': user.get_role_display()
            }

            if user in project.likes.all():
                # Удаление лайка
                project.likes.remove(user)
                response_data['message'] = 'Лайк удален'
                response_data['liked'] = False

                # Для экспертов также удаляем голос
                if user.role == Account.Role.EXPERT and user in project.experts_voted.all():
                    project.experts_voted.remove(user)
                    response_data['expert_voted'] = False
            else:
                # Добавление лайка
                project.likes.add(user)
                response_data['message'] = 'Лайк добавлен'
                response_data['liked'] = True

                # Для экспертов также добавляем голос
                if user.role == Account.Role.EXPERT:
                    project.experts_voted.add(user)
                    response_data['expert_voted'] = True
                else:
                    response_data['expert_voted'] = False

            return Response(response_data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {'status': 'error', 'message': 'Проект не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

class ProjectCreateView(generics.CreateAPIView):
    """
    API для создания нового проекта.
    Доступно только аутентифицированным пользователям.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            owner=user,
            initiator=user,
            customer=user if hasattr(user, "company_name") and user.company_name else None
        )


class ProjectUpdateView(generics.UpdateAPIView):
    """
    API для редактирования проекта.
    Редактировать может только владелец (owner).
    """
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("Вы не владелец проекта.")
        return obj

class ProjectClaimView(APIView):
    """
    API для того, чтобы заказчик мог "забрать" проект.
    Только пользователи с company_name могут выполнять это действие.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        user = request.user

        # Проверяем, что у пользователя есть company_name
        if not getattr(user, "company_name", None):
            raise PermissionDenied("Только заказчики могут забирать проекты.")

        # Если у проекта уже есть заказчик
        if project.customer:
            raise PermissionDenied("Этот проект уже имеет заказчика.")

        # Назначаем нового заказчика и владельца
        project.customer = user
        project.owner = user
        project.save()

        return Response({"detail": "Вы успешно забрали проект."})