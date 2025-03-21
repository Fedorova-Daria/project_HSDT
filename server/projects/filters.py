import django_filters
from .models import Idea

class IdeaFilter(django_filters.FilterSet):
    initiator_role = django_filters.CharFilter(
        field_name="initiator__role",
        lookup_expr="iexact"
    )

    class Meta:
        model = Idea
        fields = ["initiator_role"]

