import django_filters
from .models import Notification
from django.db import models

class NotificationFilter(django_filters.FilterSet):
    is_read = django_filters.BooleanFilter(field_name='is_read')
    user = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    type = django_filters.CharFilter(lookup_expr='iexact')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    # Фильтры по связанным объектам
    related_team = django_filters.NumberFilter(
        field_name='related_team_join_request__team__id',
        lookup_expr='exact'
    )
    related_project = django_filters.NumberFilter(
        field_name='related_project_application__project__id',
        lookup_expr='exact'
    )

    class Meta:
        model = Notification
        fields = [
            'user',
            'is_read',
            'type',
            'created_after',
            'created_before',
            'related_team',
            'related_project'
        ]

    # Добавляем сортировку
    order_by = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('is_read', 'is_read'),
        ),
        field_labels={
            'created_at': 'Дате создания',
            'is_read': 'Статусу прочтения',
        }
    )
    class Meta:
        model = Notification
        fields = ['is_read']

