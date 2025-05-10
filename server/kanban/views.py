from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Board, Column, Task
from .serializers import BoardSerializer, ColumnSerializer, TaskSerializer

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Получаем данные доски
        board_data = request.data
        team_id = board_data.get('team')  # Получаем team_id

        # Проверка на наличие team_id
        if not team_id:
            return Response({"error": "Team ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем доску
        board = Board.objects.create(team_id=team_id)

        # Проверка на колонки и их добавление
        columns_data = board_data.get('columns', [])
        for col_data in columns_data:
            Column.objects.create(board=board, **col_data)

        # Возвращаем сериализованный ответ с доской
        return Response(BoardSerializer(board).data, status=status.HTTP_201_CREATED)

class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

    @action(detail=True, methods=['post'])
    def reorder(self, request, pk=None):
        column = self.get_object()
        new_order = request.data.get("order")
        if new_order is not None:
            column.order = new_order
            column.save()
            return Response({"status": "reordered"}, status=status.HTTP_200_OK)
        return Response({"error": "No order provided"}, status=status.HTTP_400_BAD_REQUEST)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['post'])
    def reorder(self, request, pk=None):
        task = self.get_object()
        new_column_id = request.data.get("column")
        new_order = request.data.get("order")

        if new_column_id is not None and new_order is not None:
            task.column_id = new_column_id  # Обновляем колонку
            task.order = new_order  # Обновляем порядок
            task.save()
            return Response({"status": "reordered"}, status=status.HTTP_200_OK)
        
        return Response({"error": "No column or order provided"}, status=status.HTTP_400_BAD_REQUEST)