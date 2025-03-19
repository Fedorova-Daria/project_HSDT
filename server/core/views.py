from rest_framework import generics
from .models import UniversityGroup, Technology
from .serializers import GroupSerializer, TechnologySerializer


class GroupListView(generics.ListAPIView):
    queryset = UniversityGroup.objects.all()
    serializer_class = GroupSerializer

class TechnologyListView(generics.ListAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


