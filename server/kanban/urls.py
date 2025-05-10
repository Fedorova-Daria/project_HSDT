from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet, ColumnViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'boards', BoardViewSet)
router.register(r'columns', ColumnViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('kanban/', include(router.urls)),
]