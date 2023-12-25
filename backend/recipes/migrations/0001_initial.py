# Generated by Django 3.2.3 on 2023-12-25 13:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Минимальное количество ингредиентов')], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Состав рецепта',
                'verbose_name_plural': 'Составы рецептов',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Введите название', max_length=150, verbose_name='Название')),
                ('image', models.ImageField(help_text='Загрузите изображение', upload_to='media/', verbose_name='Изображение')),
                ('text', models.TextField(help_text='Опишите приготовление', null=True, verbose_name='Описание')),
                ('cooking_time', models.IntegerField(help_text='Укажите время приготовления', null=True, validators=[django.core.validators.MinValueValidator(1, 'Минимальное время - 1 минута')], verbose_name='Время приготовления')),
                ('pub_data', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['id'],
            },
        ),
    ]
