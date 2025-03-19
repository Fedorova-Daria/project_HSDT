# core/urls.py

from django.urls import path
from .views import GroupListView, TechnologyListView

urlpatterns = [
    path('university_groups', GroupListView.as_view(), name='group-list'),  # API для получения списка групп
    path('technologies', TechnologyListView.as_view(), name='technology-list'),
]

