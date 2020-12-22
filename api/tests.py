import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Dog, Breed
from .serializers import DogSerializer, BreedSerializer

client = APIClient()

class TestGetDogs(TestCase):
    """ Тестирует получение данных одной/всех собак """
    def setUp(self):
        self.breed1 = Breed.objects.create(
            title='Лабрадор', description='Обычный')
        self.dog1 = Dog.objects.create(
            name='Romulus', sex='MALE', coat_color='brown',
            behavior='CALM', breed=self.breed1, age=2)
        Dog.objects.create(
            name='Anka', sex='MALE', coat_color='black',
            behavior='AGRESSIVE', breed=self.breed1, age=2)

    def test_get_dogs(self):
        """Тестирует получение всех собак"""
        response = client.get('/api/v1/dogs/')
        dogs = Dog.objects.all()
        serializer = DogSerializer(dogs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_one_dog(self):
        """
        Тестирует получение одной собаки
        по правильной ссылке
        
        """
        response = client.get('/api/v1/dogs/1/')
        dog = Dog.objects.get(id=1)
        serializer = DogSerializer(dog)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_one_dog(self):
        """
        Тестирует получание одной собаки 
        по неправильной ссылке
        
        """
        response = client.get('/api/v1/dogs/10/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_search_dogs(self):
        """
        Тестирует поиск собак по кличке
        """
        response = client.get('/api/v1/dogs/?search=Romulus')
        dog = Dog.objects.get(name='Romulus')
        serializer = DogSerializer(dog)
        self.assertEqual(response.json(), [serializer.data])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCreateDog(TestCase):
    """Тестирует создание собак"""
    def setUp(self):
        #Образец со всеми заполненными полями
        self.valid_dog_1 = {
            'name': 'Romulus',
            'sex': 'Мужской',
            'coat_color': 'black',
            'behavior': 'Агрессивный',
            'breed': 'Sheepdog',
            'age': 5
        }
        #Образец с минимальными количеством заполненных полей
        self.valid_dog_2 = {
            'name': 'Romulus',
            'breed': 'Sheepdog',
            'age': 5,
        }
        # Образец с незаполненным именем
        self.invalid_dog = {
            'name': '',
            'sex': 'Женский',
            'coat_color': 'зеленый',
            'behavior': 'Спокойный',
            'breed': 'Sheepdog'
        }

    def test_create_valid_dog(self):
        """Тестирует создание собаки по с правильными исходными"""
        response_1 = client.post(
            '/api/v1/dogs/',
            data=json.dumps(self.valid_dog_1),
            content_type='application/json'
        )
        response_2 = client.post(
            '/api/v1/dogs/',
            data=json.dumps(self.valid_dog_2),
            content_type='application/json'
        )
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_dog(self):
        """ Тестирует создание собаки по неправильным исходным """
        response = client.post(
            '/api/v1/dogs/',
            data=json.dumps(self.invalid_dog),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUpdateDog(TestCase):
    """Тестирует обновление данных собаки"""

    def setUp(self):
        self.breed1 = Breed.objects.create(
            title='Лабрадор', description='Обычный')
        self.dog1 = Dog.objects.create(
            name='Romulus', sex='MALE', coat_color='brown',
            behavior='CALM', breed=self.breed1, age=2)
        self.dog2 = Dog.objects.create(
            name='Remus', sex='MALE', coat_color='black',
            behavior='AGRESSIVE', breed=self.breed1, age=2)
        # Образец с заполненным именем
        self.valid_dog = {
            'name': 'Romulus',
            'sex': 'Мужской',
            'coat_color': 'black',
            'behavior': 'Агрессивный',
            'breed': 'Sheepdog',
            'age': 5
        }
        # Образец с незаполненным именем
        self.invalid_dog = {
            'name': '',
            'sex': 'Женский',
            'coat_color': 'зеленый',
            'behavior': 'Спокойный',
            'breed': 'Sheepdog'
        }
    def test_valid_update_dog(self):
        """Тестирует обновление данных собаки по правильным исходным"""
        response = client.put(
            '/api/v1/dogs/1/',
            data=json.dumps(self.valid_dog),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_dog(self):
        """Тестирует обновление данных собаки по неправильным исходным"""
        response = client.put(
            '/api/v1/dogs/2/',
            data=json.dumps(self.invalid_dog),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDeleteDog(TestCase):
    """Тестирует удаление объекта собаки"""
    
    def setUp(self):
        self.breed = Breed.objects.create(
            title='Лабрадор', description='Обычный')
        self.dog1 = Dog.objects.create(
            name='Romulus', sex='MALE', coat_color='brown',
            behavior='CALM', breed=self.breed, age=2)
    
    def test_delete_dog(self):
        response = client.delete('/api/v1/dogs/1/')
        count = Dog.objects.all().count()
        self.assertEqual(0, count)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class TestGetBreed(TestCase):
    """Тестирует получение данных одной/нескольких пород"""

    def setUp(self):
        Breed.objects.create(
            title='Лабрадор', description='Обычный')
        Breed.objects.create(
            title='Дворняга', description='Великая')

    def test_get_breeds(self):
        """Тестирует получание данных всех пород"""
        response = client.get('/api/v1/breeds/')
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_one_breed(self):
        """
        Тестирует получение данных одной породы
        по правильным исходным данным"""
        response = client.get('/api/v1/breeds/1/')
        breed = Breed.objects.get(id=1)
        serializer = BreedSerializer(breed)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_one_breed(self):
        """
        Тестирует получение данных одной собаки
        по неправильным исходным (имя)
        """
        response = client.get('/api/v1/breeds/10/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
class TestCreateBreed(TestCase):
    """Тестирует создание новой породы"""

    def setUp(self):
        self.valid_breed = {
            'title': 'Rome',
            'description': 'SPQR',
        }
        self.invalid_breed = {
            'title': '',
            'description': 'SPQR',
        }

    def test_create_valid_breed(self):
        """Тестирует создание новой породы с правильными исходными"""
        response = client.post(
            '/api/v1/breeds/',
            data=json.dumps(self.valid_breed),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_breed(self):
        """Тестирует создание породы с неправильными исходными(название)"""
        response = client.post(
            '/api/v1/breeds/',
            data=json.dumps(self.invalid_breed),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestUpdateBreed(TestCase):
    """Тестирует обнновление данных породы"""

    def setUp(self):
        Breed.objects.create(
            title='Лабрадор', description='Обычный')
        Breed.objects.create(
            title='Дворняга', description='Великая')
        self.valid_breed = {
            'title': 'Rome',
            'description': 'SPQR',
        }
        self.invalid_breed = {
            'title': '',
            'description': 'SPQR',
        }

    def test_valid_update_breed(self):
        """Тестирует обновление данных породы
        с правильными исходными"""
        response = client.put(
            '/api/v1/breeds/1/',
            data=json.dumps(self.valid_breed),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_breed(self):
        """Тестирует обновленме данных породы
        с неправильными исходными (название)"""
        response = client.put(
            '/api/v1/breeds/1/',
            data=json.dumps(self.invalid_breed),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDeteteBreed(TestCase):

    def setUp(self):
        self.breed = Breed.objects.create(
            title='Лабрадор', description='Обычный')
    
    def test_delete_breed(self):
        """Тестирует удаление данных породы """
        response = client.delete('/api/v1/breeds/1/')
        count = Breed.objects.all().count()
        self.assertEqual(0, count)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
