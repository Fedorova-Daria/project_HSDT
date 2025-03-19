from rest_framework import serializers
from .models import Idea

class IdeaSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Idea
        fields = "__all__"  # Вернёт все поля модели + likes_count
        extra_kwargs = {"likes": {"read_only": True}}  # Лайки нельзя передавать вручную

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

