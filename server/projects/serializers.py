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


# Сериализатор для создания проекта
class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "description", "status", "is_hiring"]  # Только редактируемые поля