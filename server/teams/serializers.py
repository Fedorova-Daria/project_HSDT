from rest_framework import serializers
from .models import Team, TeamJoinRequest
from users.models import Account  # Убедись, что ты используешь свою модель
from users.serializers import AccountShortSerializer  # Имя, почта, навыки и т.д.

class TeamCreateSerializer(serializers.ModelSerializer):
    members_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    class Meta:
        model = Team
        fields = ['name', 'description', 'members_ids']

    def validate(self, data):
        request = self.context["request"]
        if not request.user.role == 'ST':  # Предполагаем, что у Account есть поле role
            raise serializers.ValidationError("Создавать команды могут только студенты.")
        return data

    def create(self, validated_data):
        members_ids = validated_data.pop("members_ids", [])
        team = Team.objects.create(owner=self.context["request"].user, **validated_data)
        team.members.add(self.context["request"].user)  # Автоматическое добавление владельца
        for uid in members_ids:
            try:
                user = Account.objects.get(id=uid)
                team.members.add(user)
            except Account.DoesNotExist:
                continue
        return team


class TeamListSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    members_ids = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'members_ids', 'status', 'skills']

    def get_members_ids(self, obj):
        return list(obj.members.values_list('id', flat=True))

    def get_skills(self, obj):
        skills_set = set()
        for member in obj.members.all():
            skills_set.update(member.skills.values_list('name', flat=True))
        skills = list(skills_set)
        if len(skills) > 4:
            return skills[:4] + [f"+{len(skills) - 4}"]
        return skills


class TeamDetailSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    owner_name = serializers.SerializerMethodField()
    members = AccountShortSerializer(many=True)
    skills = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'owner_name', 'status', 'skills', 'members', 'owner']

    def get_owner_name(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}"

    def get_skills(self, obj):
        skills_set = set()
        for member in obj.members.all():
            skills_set.update(member.skills.values_list('name', flat=True))
        return list(skills_set)


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description', 'status']

    def validate_status(self, value):
        if self.instance and self.context["request"].user != self.instance.owner:
            raise serializers.ValidationError("Только тим-лид может менять статус.")
        return value


class TeamJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamJoinRequest
        fields = "__all__"
        read_only_fields = ("user", "status", "created_at")  # status пусть юзер тоже не задаёт

