from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters

from .models import Dog, Breed
from .serializers import DogSerializer, BreedSerializer


class DogsViewSet(viewsets.ModelViewSet):
    """Выполняет CRUD методы для модели Dog (Собака)"""
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    def perform_create(self, serializer):
        """
         Метод приводит название породы в к единому стилю,
        добавляет объект породы в создаваемый объект собаки,
        Если объекта породы нет, то сначала создает его.
        
        """
        title = serializer.validated_data['breed']
        title = title['title'].capitalize()
        breed = Breed.objects.get_or_create(title=title)
        serializer.save(breed=breed[0])

    def perform_update(self, serializer):
        title = serializer.validated_data['breed']
        title = title['title'].capitalize()
        breed = Breed.objects.get_or_create(title=title)
        serializer.save(breed=breed[0])




class BreedViewSet(viewsets.ModelViewSet):
    """Выполняет CRUD методы для модели Breed (Порода)"""
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer



