from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IdeaViewSet, ProjectApplicationViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'ideas', IdeaViewSet, basename='ideas')
router.register(r'project-applications', ProjectApplicationViewSet)

urlpatterns = router.urls



