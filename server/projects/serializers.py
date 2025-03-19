from rest_framework import serializers
from .models import Idea
from users.models import Account
from core.models import Technology

class IdeaSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    confirmed = serializers.SerializerMethodField()
    initiator_info = serializers.SerializerMethodField()
    experts_voted_info = serializers.SerializerMethodField()
    technologies_info = serializers.SerializerMethodField()

    class Meta:
        model = Idea
        fields = [
            "id", "name", "description", "short_description", "likes_count",
            "confirmed", "initiator_info", "experts_voted_info", "technologies_info",
            "created_at"
        ]

    def get_confirmed(self, obj):
        return obj.experts_voted.count() >= obj.votes_to_approve

    def get_initiator_info(self, obj):
        if not obj.initiator:
            return None
        owner = obj.initiator
        return {
            "id": owner.id,
            "role": owner.role,
            "name": owner.company_name if owner.role == Account.Role.CUSTOMER else f"{owner.first_name} {owner.last_name}"
        }

    def get_experts_voted_info(self, obj):
        return [{"id": expert.id, "name": f"{expert.first_name} {expert.last_name}"} for expert in obj.experts_voted.all()]

    def get_technologies_info(self, obj):
        return [{"id": tech.id, "name": tech.name} for tech in obj.technologies.all()]



class IdeaShortSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    experts_voted_ids = serializers.PrimaryKeyRelatedField(
        many=True, source="experts_voted", read_only=True
    )

    class Meta:
        model = Idea
        fields = ["id", "title", "likes_count", "experts_voted_ids"]

class IdeaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        exclude = ["likes", "experts_voted"]  # Эти поля нельзя передавать при создании

