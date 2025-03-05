from django.urls import path
from .views import LoginView, RegistrationView, UserProfileView, RefreshTokenView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path("me/", UserProfileView.as_view(), name="user-profile"),
    path("token/refresh/", RefreshTokenView.as_view(), name='refresh_token')
]

