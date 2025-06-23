from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IdeaViewSet, ProjectApplicationViewSet, ProjectParticipantsDetailsView, ProjectParticipantRatingViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'ideas', IdeaViewSet, basename='ideas')
router.register(r'project-applications', ProjectApplicationViewSet)
router.register(r'participant-ratings', ProjectParticipantRatingViewSet, basename='participant-ratings')

urlpatterns = [
    # 👇 твой кастомный путь
    path('projects/<int:pk>/participants-details/', ProjectParticipantsDetailsView.as_view(), name='project-participants-details'),
    path('add_project_to_team/<int:team_id>/<int:project_id>/', views.add_project_to_team, name='add_project_to_team'),
    path('add_idea_to_team/<int:team_id>/<int:idea_id>/', views.add_idea_to_team, name='add_idea_to_team'),
]

# 👇 добавляем маршруты из router
urlpatterns += router.urls

