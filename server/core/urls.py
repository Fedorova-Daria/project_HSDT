from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GroupListView, TechnologyListView, SemesterViewSet

router = DefaultRouter()
router.register(r'semesters', SemesterViewSet, basename='semester')

urlpatterns = [
    path('university_groups', GroupListView.as_view(), name='group-list'),
    path('technologies', TechnologyListView.as_view(), name='technology-list'),
] + router.urls