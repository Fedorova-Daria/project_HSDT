from django.urls import path
from .views import ProjectListView, ProjectLikeView, ProjectCreateView, ProjectUpdateView, ProjectClaimView
from .views import ProjectApplicationView, ProjectSelectWorkersView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:project_id>/like/', ProjectLikeView.as_view(), name='project-like'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-edit'),
    path('<int:pk>/claim/', ProjectClaimView.as_view(), name='project-claim'),
    path('<int:project_id>/apply/', ProjectApplicationView.as_view(), name='project-apply'),
    path('<int:project_id>/selectworkers/', ProjectSelectWorkersView.as_view(), name='select-workers'),
]


