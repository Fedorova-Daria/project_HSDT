# core/serializers.py

from rest_framework import serializers
from .models import UniversityGroup, Technology


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityGroup
        fields = ["id", "name"]

class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["id", "name"]

