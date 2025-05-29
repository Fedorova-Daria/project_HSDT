# projects/serializers.py

from rest_framework import serializers
from .models import Project, Idea, ProjectApplication, ProjectParticipantRating, Semester, ProjectMessage, Institute
from users.serializers import AccountShortSerializer
from core.serializers import TechnologySerializer
from teams.models import Team
from users.models import Account
import json

class ProjectSerializer(serializers.ModelSerializer):
    initiator = AccountShortSerializer(read_only=True)
    owner = AccountShortSerializer(read_only=True)
    expert_likes = AccountShortSerializer(many=True, read_only=True)
    workers = AccountShortSerializer(many=True, read_only=True)
    teams = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), many=True)
    favorites = AccountShortSerializer(many=True, read_only=True)
    skills_required = TechnologySerializer(many=True, read_only=True)
    semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all())

    institutes = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_institutes(self, obj):
        try:
            # распарси JSON из CharField
            institutes_list = json.loads(obj.institutes)
            # можно вернуть список кодов или имён
            return institutes_list
        except Exception:
            return []


class ProjectUpdateSerializer(serializers.ModelSerializer):
    institutes = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    institutes_read = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'title', 'description', 'status', 'owner', 'initiator',
            'skills_required', 'semester', 'institutes', 'institutes_read'
        ]

    def get_institutes_read(self, obj):
        return obj.get_institutes_list()

    def create(self, validated_data):
        skills_data = validated_data.pop('skills_required', [])
        institutes_data = validated_data.pop('institutes', [])

        project = Project.objects.create(**validated_data)

        # Устанавливаем ManyToMany связи
        if skills_data:
            project.skills_required.set(skills_data)

        if institutes_data:
            # если у тебя institutes - поле JSON в модели, то сохраняй через метод
            project.set_institutes_list(institutes_data)
            project.save()

        return project


    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills_required', None)
        institutes_data = validated_data.pop('institutes', None)

        instance = super().update(instance, validated_data)

        if skills_data is not None:
            instance.skills_required.set(skills_data)

        if institutes_data is not None:
            instance.set_institutes_list(institutes_data)
            instance.save()

        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # получаем список из JSON-строки
        ret['institutes'] = instance.get_institutes_list()
        return ret

class ProjectMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)

    class Meta:
        model = ProjectMessage
        fields = ['id', 'project', 'sender','sender_name', 'text', 'created_at', 'is_revision_request']

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



class ProjectParticipantRatingSerializer(serializers.ModelSerializer):
    rated_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProjectParticipantRating
        fields = ['id', 'project', 'rated_user', 'rated_by', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'rated_by']

class RatedUserDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    average_rating = serializers.FloatField(allow_null=True)

class ProjectParticipantDetailSerializer(serializers.Serializer):
    workers = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()

    def get_workers(self, project):
        result = []
        for user in project.workers.all():
            ratings = ProjectParticipantRating.objects.filter(project=project, rated_user=user)
            avg = round(sum(r.rating for r in ratings) / ratings.count(), 2) if ratings.exists() else None
            result.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'average_rating': avg,
            })
        return result

    def get_teams(self, project):
        result = []
        for team in project.teams.all():
            team_data = {
                'team_id': team.id,
                'team_name': team.name,
                'members': [],
            }
            for user in team.members.all():
                ratings = ProjectParticipantRating.objects.filter(project=project, rated_user=user)
                avg = round(sum(r.rating for r in ratings) / ratings.count(), 2) if ratings.exists() else None
                team_data['members'].append({
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'average_rating': avg,
                })
            result.append(team_data)
        return result