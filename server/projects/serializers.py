# projects/serializers.py

from rest_framework import serializers
from .models import Project, Idea, ProjectApplication
from users.serializers import AccountShortSerializer
from core.serializers import TechnologySerializer
from teams.models import Team

class ProjectSerializer(serializers.ModelSerializer):
    initiator = AccountShortSerializer(read_only=True)
    owner = AccountShortSerializer(read_only=True)
    expert_likes = AccountShortSerializer(many=True, read_only=True)
    workers = AccountShortSerializer(many=True, read_only=True)
    teams = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), many=True)
    favorites = AccountShortSerializer(many=True, read_only=True)
    experts_voted = AccountShortSerializer(many=True, read_only=True)
    skills_required = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'owner', 'initiator', 'skills_required']


class ProjectUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['status', 'approved']


class IdeaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    likes_count = serializers.SerializerMethodField()
    expert_likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Idea
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_expert_likes_count(self, obj):
        return obj.expert_likes.count()

class IdeaEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ['title', 'description', 'skills_required', 'status']


class ProjectApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectApplication
        fields = '__all__'
        read_only_fields = ('status', 'created_at')


