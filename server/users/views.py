from rest_framework import generics
from .models import Account
from .serializers import AccountSerializer
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated


def create_jwt_tokens(user):
    """
    Функция для создания JWT токенов для пользователя
    """
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh)
    }


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = Account.objects.get(email=email)  # Ищем пользователя по email
        except Account.DoesNotExist:
            return Response({"success": False,
                             "email_is_correct": False,
                             "message": "Invalid credentials"
                             }, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем пароль
        if check_password(password, user.password):
            tokens = create_jwt_tokens(user)
            return Response({
                "success": True,
                "email_is_correct": True,
                "message": "Login successful",
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"]
            }, status=status.HTTP_200_OK)

        return Response({"success": False, 
                         "email_is_correct": True, 
                         "message": "Invalid credentials"
                         }, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(TokenRefreshView):
    pass  # Просто используем стандартное обновление


class RegistrationView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()  # Сохраняем нового пользователя
            # Создаем JWT токены
            tokens = create_jwt_tokens(user)
            return Response({
                "success": True,
                "message": "User registered successfully",
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"]
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Только авторизованные юзеры

    def get(self, request):
        user = request.user  # Django сам найдет юзера по JWT токену
        serializer = AccountSerializer(user)
        return Response(serializer.data)


