import django_filters
from projects.models import Project

class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = {
            'visible': ['exact'],
        }