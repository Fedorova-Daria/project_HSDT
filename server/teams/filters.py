import django_filters
from teams.models import TeamJoinRequest, Team

class TeamJoinRequestFilter(django_filters.FilterSet):
    team = django_filters.NumberFilter(field_name='team__id', lookup_expr='exact')
    status = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = TeamJoinRequest
        fields = ['team', 'status']

class TeamFilter(django_filters.FilterSet): # !!!
    owner = django_filters.NumberFilter(field_name='owner__id', lookup_expr='exact') # !!!
    members_ids = django_filters.NumberFilter(field_name='members__id', lookup_expr='exact') # !!!
    status = django_filters.CharFilter(method='filter_status') # !!!
    
    def filter_status(self, queryset, name, value): # !!!
        if value:
            statuses = value.split(',') # !!!
            return queryset.filter(status__in=statuses) # !!!
        return queryset # !!!

    class Meta:
        model = Team
        fields = ['owner', 'status', 'members_ids']
