from rest_framework import serializers
from .models import Project
from users.models import Account

# Сериализатор для заказчика
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'avatar']

# Сериализатор для пользователя
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'avatar']

# Сериализатор для проекта в листе
class ProjectListSerializer(serializers.ModelSerializer):
    initiator = serializers.StringRelatedField()  # Покажет имя инициатора
    customer = AccountSerializer(allow_null=True)  # Добавляем информацию о заказчике
    applicants = AccountSerializer(allow_null=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)  # Количество лайков
    applicants_count = serializers.IntegerField(source="applicants.count", read_only=True)  # Количество откликнувшихся
    workers = AccountSerializer(many=True, read_only=True)  # Проголосовавшие эксперты (или работающие пользователи)

    class Meta:
        model = Project
        fields = "__all__"  # Включаем все поля из модели + добавленные через сериализаторы

# Сериализатор для создания проекта
class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "description", "status", "is_hiring"]  # Только редактируемые поля