from django.urls import path
from .views import ProjectListView, ProjectLikeView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:project_id>/like/', ProjectLikeView.as_view(), name='project-like'),
]


