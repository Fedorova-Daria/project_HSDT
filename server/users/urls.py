from django.urls import path
from .views import AccountListCreateView


urlpatterns = [
    path('users/', AccountListCreateView.as_view(), name='user-list'),
]

