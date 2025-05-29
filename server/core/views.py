from rest_framework import generics, viewsets
from .models import UniversityGroup, Technology, Semester
from .serializers import GroupSerializer, TechnologySerializer, SemesterSerializer


class GroupListView(generics.ListAPIView):
    queryset = UniversityGroup.objects.all()
    serializer_class = GroupSerializer

class TechnologyListView(generics.ListAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


class SemesterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Semester.objects.all().order_by('-year', 'semester')
    serializer_class = SemesterSerializer