from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters

from .models import Dog, Breed
from .serializers import DogSerializer, BreedSerializer
from .utils import create_or_update


class DogsViewSet(viewsets.ModelViewSet):
    """Выполняет CRUD операции для модели Dog (Собака)"""
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    def perform_create(self, serializer):
        breed = create_or_update(serializer)
        serializer.save(breed=breed[0])

    def perform_update(self, serializer):
        breed = create_or_update(serializer)
        serializer.save(breed=breed[0])


class BreedViewSet(viewsets.ModelViewSet):
    """Выполняет CRUD операции для модели Breed (Порода)"""
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer



