from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Idea
from users.models import Account
from .serializers import IdeaSerializer, IdeaShortSerializer, IdeaCreateSerializer
from django.shortcuts import get_object_or_404

class IdeaListView(ListAPIView):
    """Список идей (доступен всем)"""
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [AllowAny]  # Доступ для всех, в том числе анонимных пользователей

class IdeaDetailView(RetrieveAPIView):
    """Детальный просмотр идеи"""
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [AllowAny]  # Доступ для всех

class VoteIdeaView(APIView):
    """Голосование за идею (только для авторизованных)"""
    permission_classes = [IsAuthenticated]

    def post(self, request, idea_id):
        idea = get_object_or_404(Idea, id=idea_id)
        user = request.user

        user_has_liked = idea.likes.filter(id=user.id).exists()
        user_is_expert = user.role == Account.Role.EXPERT
        user_is_voted_expert = idea.experts_voted.filter(id=user.id).exists()

        # Если пользователь уже лайкал - снимаем лайк
        if user_has_liked:
            idea.likes.remove(user)
            if user_is_voted_expert:
                idea.experts_voted.remove(user)

            return Response({"message": "Лайк удалён"}, status=status.HTTP_200_OK)

        # Если пользователь эксперт, его голос идёт в зачет
        if user_is_expert:
            print("эксперт?")
            idea.experts_voted.add(user)

        idea.likes.add(user)

        return Response({"message": "Голос/лайк добавлен"}, status=status.HTTP_200_OK)

class IdeaCreateView(CreateAPIView):
    """Создание новой идеи (только для авторизованных)"""
    queryset = Idea.objects.all()
    serializer_class = IdeaCreateSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные юзеры

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)  # Инициатором становится текущий пользователь
