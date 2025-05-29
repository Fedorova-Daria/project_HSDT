# core/serializers.py

from rest_framework import serializers
from .models import UniversityGroup, Technology, Semester


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityGroup
        fields = "__all__"

class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = "__all__"

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'year', 'semester']