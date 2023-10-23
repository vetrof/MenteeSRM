from rest_framework import serializers
from courses.models import Lesson, Topic


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'  # Используем все поля модели Lesson

    # def create(self, validated_data):
    #     """
    #     Метод для создания нового урока
    #     """
    #     return Lesson.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Метод для обновления существующего урока
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.info = validated_data.get('info', instance.info)
    #     # Добавьте другие поля модели, которые вы хотите обновить
    #
    #     instance.save()
    #     return instance
