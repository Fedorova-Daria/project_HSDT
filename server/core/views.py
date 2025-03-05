from rest_framework import generics
from .models import Group
from .serializers import GroupSerializer


class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


