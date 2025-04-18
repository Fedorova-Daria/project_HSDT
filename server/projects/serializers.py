# projects/serializers.py

from rest_framework import serializers
from .models import Project, Idea, TeamResponse
from users.serializers import AccountShortSerializer
from core.serializers import TechnologySerializer

class ProjectSerializer(serializers.ModelSerializer):
    initiator = AccountShortSerializer(read_only=True)
    customer = AccountShortSerializer(read_only=True)
    owner = AccountShortSerializer(read_only=True)

    likes = AccountShortSerializer(many=True, read_only=True)
    expert_likes = AccountShortSerializer(many=True, read_only=True)
    applicants = AccountShortSerializer(many=True, read_only=True)
    workers = AccountShortSerializer(many=True, read_only=True)
    favorites = AccountShortSerializer(many=True, read_only=True)
    experts_voted = AccountShortSerializer(many=True, read_only=True)

    skills_required = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = [
            'approved', 'likes', 'favorites', 'applicants', 'workers', 'experts_voted',
            'created_at', 'expert_likes', 'votes_to_approve'
        ]
        read_only_fields = ['initiator', 'owner']

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


class TeamResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamResponse
        fields = ['id', 'project', 'team', 'created_at']

