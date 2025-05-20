import django_filters
from projects.models import Project, Idea



class ProjectFilter(django_filters.FilterSet):
    technology_type = django_filters.CharFilter(
        field_name='skills_required__type', lookup_expr='exact'
    )

    class Meta:
        model = Project
        fields = ['visible']

class IdeaFilter(django_filters.FilterSet):
    technology_type = django_filters.CharFilter(
        field_name='skills_required__type', lookup_expr='exact'
    )

    class Meta:
        model = Idea
        fields = ['technology_type']