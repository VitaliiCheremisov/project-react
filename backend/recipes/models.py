from django.contrib.auth import get_user_model
from django.core.validators import (MinValueValidator,
                                    ValidationError)
from django.db import models

from foodgram import constants
from tags.models import Tag

CustomUser = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиетов."""
    name = models.CharField(
        max_length=constants.MAX_INGREDIENT_LENGTH,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=constants.MAX_UNIT_LENGTH,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        max_length=constants.MAX_RECIPE_NAME_LENGTH,
        verbose_name='Название',
        help_text='Введите название'
    )
    image = models.ImageField(
        upload_to='media/',
        verbose_name='Изображение',
        help_text='Загрузите изображение',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Опишите приготовление'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipes',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэг'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления',
        validators=[MinValueValidator(
            1, 'Минимальное время - 1 минута'
        )]
    )
    pub_data = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-pub_data', 'id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe'
            )
        ]

    def clean(self):
        """Проверка на создание рецепта без ингредиентов."""
        try:
            self.ingredients.exists()
        except ValueError:
            raise ValidationError(
                'Нельзя создавать рецепт без ингредиентов.'
            )

    def __str__(self):
        return f'{self.name} - автор: {self.author.username}'


class IngredientRecipes(models.Model):
    """Промежуточная модель с ингредиентами для рецепта."""
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты'
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(
                1, ' Минимальное количество ингредиентов'
            ),
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Состав рецепта'
        verbose_name_plural = 'Составы рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipes', 'ingredients'],
                name='unique_ingredients'
            )
        ]

    def __str__(self):
        return f'{self.recipes.name} - {self.ingredients.name}'
