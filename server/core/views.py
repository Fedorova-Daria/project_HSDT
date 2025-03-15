from rest_framework import generics
from .models import UniversityGroup
from .serializers import GroupSerializer


class GroupListView(generics.ListAPIView):
    queryset = UniversityGroup.objects.all()
    serializer_class = GroupSerializer


