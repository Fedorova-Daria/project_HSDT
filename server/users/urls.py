from django.urls import path
from .views import LoginView, RegistrationView, AccountMeView, RefreshTokenView, AccountIDView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path("me/", AccountMeView.as_view(), name="user-profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("<int:id>/", AccountIDView.as_view(), name="user-detail")
]

