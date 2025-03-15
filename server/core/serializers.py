# core/serializers.py

from rest_framework import serializers
from .models import UniversityGroup


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityGroup
        fields = ["id", "name"]

