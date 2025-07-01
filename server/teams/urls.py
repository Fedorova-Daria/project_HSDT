from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, TeamJoinRequestViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'team-join-requests', TeamJoinRequestViewSet, basename='join-request')

urlpatterns = [
    path('', include(router.urls)),
]