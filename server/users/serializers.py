from rest_framework import serializers
from .models import Account, UserActivity
from django.contrib.auth.hashers import make_password
from core.models import UniversityGroup
from core.serializers import TechnologySerializer


class AccountSerializer(serializers.ModelSerializer):
    university_group = serializers.PrimaryKeyRelatedField(queryset=UniversityGroup.objects.all(), required=False)
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'company_name',
                    'university_group', 'role', 'phone', 'bio', 'skills', 'avatar', 'created_at', 'mode']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False},
            'bio': {'required': False},
            'avatar': {'required': False},
        }

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills', None)
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)

        if skills_data is not None:
            # Обновляем ManyToMany поле skills
            instance.skills.set(skills_data)

        return instance

    def create(self, validated_data):
        if "username" not in validated_data:
            validated_data["username"] = validated_data["email"]  # Если нет username, ставим email

        # Хешируем пароль перед сохранением
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        # Создаем пользователя
        return super().create(validated_data)


class AccountShortSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'id',
            'email',
            'full_name',
            'avatar',
            'role',
            'role_display',
            'university_group',
            'total_rating',
            'company_name',
            'skills',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name or ''} {obj.last_name or ''}".strip() or obj.email

    def get_role_display(self, obj):
        return obj.get_role_display()
    

class UserActivitySerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    team_id = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()

    class Meta:
        model = UserActivity
        fields = ["type", "team_id", "project_id", "started_at", "ended_at"]

    def get_type(self, obj):
        return "team" if obj.team else "project"

    def get_team_id(self, obj):
        return obj.team.id if obj.team else None

    def get_project_id(self, obj):
        return obj.project.id if obj.project else None
    

