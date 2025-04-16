from django.urls import path
from .views import (
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamMembersView,
    TeamWithdrawRequestView,
    TeamJoinView,
    TeamLeaveView,
    TeamRequestView,
)

urlpatterns = [
    path('', TeamListView.as_view(), name='team-list'),
    path('<int:team_id>/', TeamDetailView.as_view(), name='team-detail'),
    path('<int:team_id>/create/', TeamCreateView.as_view(), name='team-create'),
    path('<int:team_id>/edit/', TeamUpdateView.as_view(), name='team-edit'),

    # Управление участниками
    path('<int:team_id>/members/', TeamMembersView.as_view(), name='team-add-member'),
    path('<int:team_id>/members/<int:user_id>/', TeamMembersView.as_view(), name='team-remove-member'),

    # Заявки на вступление
    path('<int:team_id>/join/', TeamJoinView.as_view(), name='team-join'),
    path('<int:team_id>/requests/<int:request_id>/accept/', TeamRequestView.as_view(), name='team-accept-request'),
    path('<int:team_id>/requests/<int:request_id>/reject/', TeamRequestView.as_view(), name='team-reject-request'),

    # Выход и отзыв заявки
    path('<int:team_id>/leave/', TeamLeaveView.as_view(), name='team-leave'),
    path('<int:team_id>/withdraw_request/', TeamWithdrawRequestView.as_view(), name='team-withdraw-request'),
]