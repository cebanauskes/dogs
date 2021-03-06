# Generated by Django 3.1.3 on 2020-12-22 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Кличка')),
                ('sex', models.TextField(choices=[('MALE', 'Мужской'), ('FEMALE', 'Женский'), ('UNKNOWN', 'Неизвестен')], default='UNKNOWN')),
                ('coat_color', models.TextField(blank=True, null=True, verbose_name='Цвет шерсти')),
                ('behavior', models.TextField(choices=[('CALM', 'Спокойный'), ('AGRESSIVE', 'Агрессивный'), ('PLAYFUL', 'Игривый'), ('UNKNOWN', 'Неизвестен')], default='UNKNOWN', verbose_name='Поведение')),
                ('age', models.PositiveIntegerField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('breed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dogs', to='api.breed')),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
    ]
