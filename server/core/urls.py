from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GroupListView, TechnologyListView, SemesterViewSet, UniversityGroupViewSet

router = DefaultRouter()
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'university-groups', UniversityGroupViewSet, basename='university-group')  # ✅ Добавьте эту строку

urlpatterns = [
    path('university_groups', GroupListView.as_view(), name='group-list'),
    path('technologies', TechnologyListView.as_view(), name='technology-list'),
] + router.urls