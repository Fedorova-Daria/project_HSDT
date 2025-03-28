from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers, viewsets, permissions, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectCreateSerializer, ProjectListSerializer
from users.models import Account
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.perms import IsStudent, IsCustomer  # Импорт из правильного места
from .models import Project
from users.models import Account  # Для проверки ролей
from rest_framework.generics import RetrieveAPIView


class ProjectListView(generics.ListAPIView):
    """
    API endpoint для отображения списка всех проектов.
    Использует ProjectSerializer для сериализации данных.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    def get_serializer_context(self):
        # Передаем request в контекст сериализатора для проверки is_liked
        return {'request': self.request}


class ProjectDetailView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer


class ProjectLikeView(APIView):
    """
    API endpoint для добавления/удаления лайков проектов.
    - Только для авторизованных пользователей
    - Добавляет пользователя в likes при запросе
    - Удаляет лайк, если пользователь уже лайкнул
    - Для экспертов также добавляет/удаляет голос в experts_voted
    - Автоматически обновляет поле approved, если собрано достаточное количество голосов
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            user = request.user

            if user in project.likes.all():
                # Удаление лайка
                project.likes.remove(user)
                message = "Лайк удален"
                liked = False

                # Для экспертов также удаляем голос
                if user.role == Account.Role.EXPERT and user in project.experts_voted.all():
                    project.experts_voted.remove(user)

            else:
                # Добавление лайка
                project.likes.add(user)
                message = "Лайк добавлен"
                liked = True

                # Для экспертов также добавляем голос
                if user.role == Account.Role.EXPERT:
                    project.experts_voted.add(user)

            # Проверяем, достаточно ли голосов для одобрения
            project.approved = project.experts_voted.count() >= project.votes_to_approve
            project.save()

            return Response(
                {
                    "status": "success",
                    "message": message,
                    "likes_count": project.likes.count(),
                    "experts_voted_count": project.experts_voted.count(),
                    "approved": project.approved,
                    "liked": liked,
                    "expert_voted": user in project.experts_voted.all(),
                },
                status=status.HTTP_200_OK,
            )

        except Project.DoesNotExist:
            return Response(
                {"status": "error", "message": "Проект не найден"},
                status=status.HTTP_404_NOT_FOUND,
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

        # Проверяем, что проект подтвержден (approved)
        if not project.approved:
            raise PermissionDenied("Проект еще не подтвержден экспертами.")

        # Если у проекта уже есть заказчик
        if project.customer:
            raise PermissionDenied("Этот проект уже имеет заказчика.")

        # Назначаем нового заказчика и владельца
        project.customer = user
        project.owner = user
        project.save()

        return Response({"detail": "Вы успешно забрали проект."})


class ProjectApplicationView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            user = request.user

            if not project.is_hiring:
                return Response(
                    {'status': 'error', 'message': 'Проект не принимает заявки'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user in project.workers.all():
                return Response(
                    {'status': 'error', 'message': 'Вы уже работаете над этим проектом'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user in project.applicants.all():
                project.applicants.remove(user)
                message = 'Заявка отозвана'
                applied = False
            else:
                project.applicants.add(user)
                message = 'Заявка подана'
                applied = True

            return Response({
                'status': 'success',
                'message': message,
                'applied': applied,
                'applicants_count': project.applicants.count()
            }, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {'status': 'error', 'message': 'Проект не найден'},
                status=status.HTTP_404_NOT_FOUND
            )


class ProjectSelectWorkersView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            user_ids = request.data.get('user_ids', [])

            # Проверяем что прислан список ID
            if not isinstance(user_ids, list):
                return Response(
                    {'error': 'user_ids должен быть списком'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Получаем всех applicants проекта
            current_applicants = project.applicants.all()
            errors = []
            added_users = []

            for user_id in user_ids:
                try:
                    user = Account.objects.get(id=user_id)

                    # Проверяем что пользователь в applicants
                    if user not in current_applicants:
                        errors.append(f'Пользователь {user_id} не подавал заявку')
                        continue

                    # Добавляем в workers если еще не там
                    if user not in project.workers.all():
                        project.workers.add(user)
                        added_users.append(user_id)

                except Account.DoesNotExist:
                    errors.append(f'Пользователь {user_id} не найден')

            if errors:
                return Response(
                    {
                        'status': 'partial_success',
                        'added': added_users,
                        'errors': errors
                    },
                    status=status.HTTP_207_MULTI_STATUS
                )

            return Response({
                'status': 'success',
                'message': 'Работники успешно добавлены',
                'added_users': added_users,
                'total_workers': project.workers.count()
            }, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {'error': 'Проект не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get_object(self):
        """Получаем проект для permission проверки"""
        return Project.objects.get(id=self.kwargs['project_id'])