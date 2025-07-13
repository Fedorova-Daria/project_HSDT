from rest_framework import generics, viewsets
from .models import UniversityGroup, Technology, Semester
from .serializers import GroupSerializer, TechnologySerializer, SemesterSerializer, UniversityGroupSerializer
from .services import StudentsTableService
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

class UniversityGroupViewSet(viewsets.ModelViewSet):
    queryset = UniversityGroup.objects.all()
    serializer_class = UniversityGroupSerializer
    
    @action(detail=False, methods=['get'])
    def students_table(self, request):
        """Получение таблицы студентов с отладкой"""
        try:
            institutes_data = StudentsTableService.get_students_hierarchy_debug()
            
            return Response({
                'success': True,
                'institutes': institutes_data,
                'total_institutes': len(institutes_data),
                'total_users': sum(
                    len(group['users']) 
                    for institute in institutes_data 
                    for group in institute['groups']
                )
            })
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
            
            return Response({
                'success': False,
                'error': str(e),
                'institutes': []
            })

class GroupListView(generics.ListAPIView):
    queryset = UniversityGroup.objects.all()
    serializer_class = GroupSerializer

class TechnologyListView(generics.ListAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


class SemesterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Semester.objects.all().order_by('-year', 'semester')
    serializer_class = SemesterSerializer