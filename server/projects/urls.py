from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IdeaViewSet, TeamRespondToProjectView, SelectTeamForProjectView
from django.urls import path

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'ideas', IdeaViewSet, basename='ideas')

urlpatterns = router.urls
urlpatterns += [
    path('projects/<int:project_id>/respond-team/', TeamRespondToProjectView.as_view()),
    path('projects/<int:project_id>/select-team/<int:team_id>/', SelectTeamForProjectView.as_view()),
]



