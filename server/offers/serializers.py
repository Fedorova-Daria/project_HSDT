from rest_framework import serializers
from .models import offers
from users.serializers import AccountShortSerializer
from teams.models import Team
from users.models import Account


class OfferSerializer(serializers.ModelSerializer):
    owner = AccountShortSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = offers
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.likes.count()


class OfferEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = offers
        fields = ['title', 'description', 'status']
