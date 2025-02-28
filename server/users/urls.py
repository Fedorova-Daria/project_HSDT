from django.urls import path
from .views import AccountListCreateView, AccountDetailView, LoginView, RegistrationView


urlpatterns = [
    path('users/', AccountListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', AccountDetailView.as_view(), name='user-detail'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/registration/', RegistrationView.as_view(), name='registration')
]

