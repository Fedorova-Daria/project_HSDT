from rest_framework import serializers
from .models import Team
from users.models import Account
from projects.models import Project


class TeamMemberSerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'avatar', 'skills')

# Вот это - вывод всей подробной инфы по командам
class TeamDetailSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True, read_only=True)
    projects = serializers.StringRelatedField(many=True)  # Можно заменить на сериализатор проектов, если надо

    class Meta:
        model = Team
        fields = '__all__'  # Включаем все поля + проекты и участников

# Это - для владельца команды и возможности её редактировать
class TeamEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'description', 'avatar', 'owner')