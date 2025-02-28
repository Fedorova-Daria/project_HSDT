from django.urls import path
from .views import AccountListCreateView, AccountDetailView, LoginView, RegistrationView


urlpatterns = [
    path('list/', AccountListCreateView.as_view(), name='user-list'),
    path('<int:pk>/', AccountDetailView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration')
]

