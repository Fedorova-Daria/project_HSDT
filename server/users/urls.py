from django.urls import path
from .views import (
    LoginView,
    RegistrationView,
    AccountMeView,
    RefreshTokenView,
    UserModeToggleAPIView,
    AccountIDView,
    UserActivityViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user-activity', UserActivityViewSet, basename='user-activity')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path("me/", AccountMeView.as_view(), name="user-profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("<int:id>/", AccountIDView.as_view(), name="user-detail"),
    path("change-theme/", UserModeToggleAPIView.as_view(), name="change-theme"),
]

urlpatterns += router.urls