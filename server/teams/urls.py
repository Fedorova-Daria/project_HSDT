from django.urls import path
from .views import (
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamMembersView
)

urlpatterns = [
    path('', TeamListView.as_view(), name='team-list'),
    path('<int:id>/', TeamDetailView.as_view(), name='team-detail'),
    path('create/', TeamCreateView.as_view(), name='team-create'),
    path('<int:id>/edit/', TeamUpdateView.as_view(), name='team-edit'),
]