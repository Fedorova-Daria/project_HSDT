import django_filters
from projects.models import Project, Idea



class ProjectFilter(django_filters.FilterSet):
    technology_type = django_filters.CharFilter(
        field_name='skills_required__type', lookup_expr='exact'
    )
    semester__year = django_filters.NumberFilter(field_name='semester__year')
    semester__semester = django_filters.CharFilter(field_name='semester__semester')
    institute = django_filters.CharFilter(method='filter_by_institute')
    status = django_filters.CharFilter(method='filter_status')

    class Meta:
        model = Project
        fields = ['visible', 'semester__year', 'semester__semester', 'institute', 'status']

    def filter_status(self, queryset, name, value):
        if value:
            # Разделяем статус на несколько значений, если передано через запятую
            statuses = value.split(',')
            return queryset.filter(status__in=statuses)
        return queryset

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