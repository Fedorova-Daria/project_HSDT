import django_filters
from .models import Board


class BoardFilter(django_filters.FilterSet):
    team = django_filters.NumberFilter(field_name='team__id', lookup_expr='exact')

    class Meta:
        model = Board
        fields = ['team']
