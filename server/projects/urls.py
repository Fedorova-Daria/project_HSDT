from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IdeaViewSet, ProjectApplicationViewSet, ProjectParticipantsDetailsView, ProjectParticipantRatingViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'ideas', IdeaViewSet, basename='ideas')
router.register(r'project-applications', ProjectApplicationViewSet)
router.register(r'participant-ratings', ProjectParticipantRatingViewSet, basename='participant-ratings')

urlpatterns = [
    # 👇 твой кастомный путь
    path('projects/<int:pk>/participants-details/', ProjectParticipantsDetailsView.as_view(), name='project-participants-details'),
]

# 👇 добавляем маршруты из router
urlpatterns += router.urls

