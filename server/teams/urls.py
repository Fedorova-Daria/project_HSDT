from django.urls import path
from .views import (
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamMembersView,
    join_team,
    accept_request,
    deny_request,
    leave_team
)

urlpatterns = [
    path('', TeamListView.as_view(), name='team-list'),
    path('<int:id>/', TeamDetailView.as_view(), name='team-detail'),
    path('create/', TeamCreateView.as_view(), name='team-create'),
    path('<int:id>/edit/', TeamUpdateView.as_view(), name='team-edit'),
    path('<int:team_id>/join', join_team),
    path('<int:team_id>/accept/<int:request_id>', accept_request),
    path('<int:team_id>/deny/<int:request_id>', deny_request),
    path('<int:team_id>/leave', leave_team),
]