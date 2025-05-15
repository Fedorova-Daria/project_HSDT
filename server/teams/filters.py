import django_filters
from teams.models import TeamJoinRequest, Team

class TeamJoinRequestFilter(django_filters.FilterSet):
    team = django_filters.NumberFilter(field_name='team__id', lookup_expr='exact')
    user = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    status = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = TeamJoinRequest
        fields = ['team', 'user', 'status']

class TeamFilter(django_filters.FilterSet):
    owner = django_filters.NumberFilter(field_name='owner__id', lookup_expr='exact')

    class Meta:
        model = Team
        fields = ['owner', 'status']  # Добавил status, так как он уже есть в модели
