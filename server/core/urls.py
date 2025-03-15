# core/urls.py

from django.urls import path
from .views import GroupListView

urlpatterns = [
    path('university_groups/list', GroupListView.as_view(), name='group-list'),  # API для получения списка групп
]

