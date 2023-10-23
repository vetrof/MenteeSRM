
from rest_framework import viewsets, status

from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.serializers import LessonsSerializer
from courses.models import Lesson

from .permissions import IsSuperuserOrReadOnly


class lessonsApiViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonsSerializer

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            # Разрешение для чтения доступно зарегистрированным пользователям
            permission_classes = [IsAuthenticated]
        else:
            # Разрешение для изменения доступно только администраторам
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]




# @api_view(['GET', 'POST'])
# def lessons_api_view(request):
#     if request.method == 'GET':
#         lessons = Lesson.objects.all()
#         serializer = LessonsSerializer(lessons, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         # Извлечение данных из запроса
#         data = request.data
#
#         # Создание и сохранение нового урока
#         serializer = LessonsSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)  # Возвращаем созданный урок и статус "Создан"
#         return Response(serializer.errors, status=400)  # Возвращаем ошибки валидации, если данные неверные
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def lesson_detail_api_view(request, lesson_id):
#     try:
#         lesson = Lesson.objects.get(pk=lesson_id)
#     except Lesson.DoesNotExist:
#         return Response(status=404)  # Урок не найден
#
#     if request.method == 'GET':
#         serializer = LessonsSerializer(lesson)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         serializer = LessonsSerializer(lesson, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         # Обработка удаления урока
#         lesson.delete()
#         return Response(status=204)  # Возвращаем статус "Без содержания"
