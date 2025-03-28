from .models import Project
from users.models import Account
from rest_framework import serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

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
class ProjectSerializer(serializers.ModelSerializer):
    initiator = serializers.StringRelatedField()  # Покажет имя инициатора
    customer = AccountSerializer(allow_null=True)  # Добавляем информацию о заказчике
    applicants = AccountSerializer(allow_null=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)  # Количество лайков
    applicants_count = serializers.IntegerField(source="applicants.count", read_only=True)  # Количество откликнувшихся
    workers = AccountSerializer(many=True, read_only=True)  # Проголосовавшие эксперты (или работающие пользователи)
    is_liked = serializers.SerializerMethodField()
    is_expert_voted = serializers.SerializerMethodField()
    experts_voted_count = serializers.IntegerField(source="experts_voted.count", read_only=True)


    class Meta:
        model = Project
        fields = "__all__"  # Включаем все поля из модели + добавленные через сериализаторы
        extra_kwargs = {
            'experts_voted': {'write_only': True}  # Скрываем в ответе, так как используем is_expert_voted
        }

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.likes.filter(id=user.id).exists()

    def get_is_expert_voted(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and hasattr(user, 'is_expert') and user.is_expert and obj.experts_voted.filter(id=user.id).exists()

# Сериалайзер для создания проекта
class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "technologies", "is_hiring", "status", "owner", "initiator", "customer"]
        read_only_fields = ["id", "owner", "initiator", "customer"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["owner"] = user
        validated_data["initiator"] = user
        if hasattr(user, "company_name") and user.company_name:
            validated_data["customer"] = user
        return super().create(validated_data)