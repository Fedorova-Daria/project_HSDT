from rest_framework import serializers
from .models import Team, TeamJoinRequest
from users.models import Account
from projects.models import Project
from users.serializers import AccountSerializer
from core.models import Technology


class TeamEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description', 'members']


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ('id', 'name')


class ProjectShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description_short', 'rating')

    def get_description_short(self, obj):
        return ' '.join(obj.description.split()[:10]) + '...' if obj.description else ''


class TeamMemberSerializer(serializers.ModelSerializer):
    skills = TechnologySerializer(many=True)

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'email', 'skills')


class TeamLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'email')


class TeamListSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    technologies = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'members_count', 'status_display', 'technologies')

    def get_members_count(self, obj):
        return obj.members.count()

    def get_technologies(self, obj):
        # Исправление фильтрации
        skills = Technology.objects.filter(users__teams=obj).distinct()[:4]
        extra = Technology.objects.filter(users__teams=obj).distinct().count() - 4
        result = [s.name for s in skills]
        if extra > 0:
            result.append(f"+{extra}")
        return result


class TeamDetailSerializer(serializers.ModelSerializer):
    leader = TeamLeaderSerializer(source='owner', read_only=True)
    members = AccountSerializer(many=True, read_only=True)
    skills = serializers.SerializerMethodField()
    projects = ProjectShortSerializer(many=True, read_only=True)
    is_leader = serializers.SerializerMethodField()
    has_pending_request = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'status', 'avatar',
                  'leader', 'members', 'skills', 'projects',
                  'is_leader', 'has_pending_request')

    def get_skills(self, obj):
        # Исправление фильтрации
        return Technology.objects.filter(users__teams=obj).values('id', 'name').distinct()

    def get_is_leader(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.owner

    def get_has_pending_request(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return TeamJoinRequest.objects.filter(
                user=request.user,
                team=obj,
                status='pending'
            ).exists()
        return False


class TeamCreateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Account.objects.filter(role='ST'),
        required=False
    )

    class Meta:
        model = Team
        fields = ('name', 'description', 'members')

    def validate_members(self, value):
        if len(value) > 10:  # Максимум 10 участников
            raise serializers.ValidationError("Максимум 10 участников в команде")
        return value

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        team = Team.objects.create(**validated_data)
        team.members.set(members)
        return team


class JoinRequestSerializer(serializers.ModelSerializer):
    user = TeamMemberSerializer(read_only=True)

    class Meta:
        model = TeamJoinRequest
        fields = ('id', 'user', 'status', 'created_at', 'message')
