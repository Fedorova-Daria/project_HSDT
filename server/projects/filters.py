import django_filters
from projects.models import Project, Idea



class ProjectFilter(django_filters.FilterSet):
    technology_type = django_filters.CharFilter(
        field_name='skills_required__type', lookup_expr='exact'
    )
    semester__year = django_filters.NumberFilter(field_name='semester__year')
    semester__semester = django_filters.CharFilter(field_name='semester__semester')
    institute = django_filters.CharFilter(method='filter_by_institute')

    class Meta:
        model = Project
        fields = ['visible', 'semester__year', 'semester__semester', 'institute']

    def filter_by_institute(self, queryset, name, value):
        # value — строка кода института, например, 'HSDT'
        return queryset.filter(institutes__icontains=f'"{value}"')

class IdeaFilter(django_filters.FilterSet):
    technology_type = django_filters.CharFilter(
        field_name='skills_required__type', lookup_expr='exact'
    )

    class Meta:
        model = Idea
        fields = ['technology_type']