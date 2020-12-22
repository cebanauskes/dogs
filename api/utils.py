from .models import Breed

def create_or_update(serializer):
    """
    Метод приводит название породы в к единому стилю,
    Если объекта породы нет, то сначала создает его.
    
    """
    title = serializer.validated_data['breed']
    title = title['title'].capitalize()
    breed = Breed.objects.get_or_create(title=title)
    return breed