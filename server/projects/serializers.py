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
class ProjectListSerializer(serializers.ModelSerializer):
    initiator = serializers.StringRelatedField()
    customer = AccountSerializer(allow_null=True)
    applicants = AccountSerializer(many=True, read_only=True)  # Изменено на many=True
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    applicants_count = serializers.IntegerField(source="applicants.count", read_only=True)
    workers = AccountSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_expert_voted = serializers.SerializerMethodField()
    experts_voted_count = serializers.IntegerField(source="experts_voted.count", read_only=True)
    is_applied = serializers.SerializerMethodField()  # Новое поле - проверка подана ли заявка текущим пользователем
    can_apply = serializers.SerializerMethodField()  # Новое поле - может ли пользователь подать заявку

    class Meta:
        model = Project
        fields = "__all__"
        extra_kwargs = {
            'experts_voted': {'write_only': True},
            'applicants': {'write_only': True}  # Скрываем applicants, так как используем is_applied
        }

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.likes.filter(id=user.id).exists()

    def get_is_expert_voted(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and user.role == Account.Role.EXPERT and obj.experts_voted.filter(
            id=user.id).exists()

    def get_is_applied(self, obj):
        """Проверяет, подал ли текущий пользователь заявку на проект"""
        user = self.context['request'].user
        return user.is_authenticated and obj.applicants.filter(id=user.id).exists()

    def get_can_apply(self, obj):
        """
        Проверяет, может ли пользователь подать заявку:
        - является студентом
        - проект открыт для найма
        - не является работником
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return False

        return (user.role == Account.Role.STUDENT and
                obj.is_hiring and
                user not in obj.workers.all())

    def get_is_customer(self, obj):
        request = self.context.get('request')
        return request and request.user.is_authenticated and obj.customer == request.user

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