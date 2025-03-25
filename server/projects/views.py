from django.shortcuts import render
from rest_framework import generics
from .models import Project
from .serializers import ProjectListSerializer


class ProjectListView(generics.ListAPIView):
    """
    API endpoint для отображения списка всех проектов.
    Использует ProjectListSerializer для сериализации данных.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer


