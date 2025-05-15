from rest_framework.routers import DefaultRouter
from .views import OfferViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = [
    path('', include(router.urls)),
]
