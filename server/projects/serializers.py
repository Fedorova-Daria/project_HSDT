from rest_framework import serializers
from .models import Idea
from users.models import Account

class IdeaSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    confirmed = serializers.SerializerMethodField()  # Для поля подтверждения

    class Meta:
        model = Idea
        fields = '__all__'

    def get_confirmed(self, obj):
        # Сравниваем количество голосов с минимально необходимым количеством
        if obj.experts_voted.count() >= obj.votes_to_approve:
            return True
        return False


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

