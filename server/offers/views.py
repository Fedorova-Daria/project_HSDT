from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from .serializers import (OfferSerializer, OfferEditSerializer)
from .models import offers

class OfferViewSet(viewsets.ModelViewSet):
    queryset = offers.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OfferEditSerializer
        return OfferSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return offers.objects.all()
        return offers.objects.filter(visible=True, status='open')

    def perform_create(self, serializer):
        # 👇 вот это добавь
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='like', permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        offers = self.get_object()
        user = request.user

        if user in idea.likes.all():
            offers.likes.remove(user)
            liked = False
        else:
            offers.likes.add(user)
            liked = True

        return Response({
            'liked': liked,
            'likes_count': offers.likes.count(),
        })




