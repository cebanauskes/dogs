from django.db import models


class Dog(models.Model):
    """Модель  Собаки
    
    name - поле с кличкой собаки
    sex - поле с выбором пола собаки
    coat_color - поле с цветом шерсти собаки
    eye_color - поле с цветом глаз собаки
    behavior - после с выбором поведения собаки
    breed - поле с породой собаки
    age - поле с возрастом собаки
    pub_date - поле с датой добавления собаки в БД
    
    """

    SEX_CHOICES = [
        ('MALE', 'Мужской'),
        ('FEMALE', 'Женский'),
        ('UNKNOWN', 'Неизвестен')
    ]

    BEHAVIOR_CHOICES = [
        ('CALM', 'Спокойный'),
        ('AGRESSIVE', 'Агрессивный'),
        ('PLAYFUL', 'Игривый'),
        ('UNKNOWN', 'Неизвестен')
    ]

    name = models.CharField('Кличка', max_length=1000)
    sex = models.TextField(
        choices=SEX_CHOICES, default='UNKNOWN')
    coat_color = models.TextField(
        'Цвет шерсти', blank=True, null=True)
    behavior = models.TextField(
        'Поведение', choices=BEHAVIOR_CHOICES, default='UNKNOWN')
    breed = models.ForeignKey(
        'Breed', on_delete=models.CASCADE,
        blank=True, null=True, related_name='dogs')
    age = models.PositiveIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ('-pub_date',)



class Breed(models.Model):
    """
    Модель породы собаки
    
    title - поле названия породы
    description - поле описания породы
    
    """
    title = models.CharField('Название', max_length=1000, unique=True)
    description = models.TextField('Описание', blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Метод делает первую букву названия заглавной,
        а все остальные строчными
        
        """
        self.title = self.title.capitalize()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
