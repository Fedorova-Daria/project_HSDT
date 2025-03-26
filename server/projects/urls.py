from django.urls import path
from .views import ProjectListView, ProjectLikeView, ProjectCreateView, ProjectUpdateView, ProjectClaimView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:project_id>/like/', ProjectLikeView.as_view(), name='project-like'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-edit'),
    path('<int:pk>/claim/', ProjectClaimView.as_view(), name='project-claim'),
]


