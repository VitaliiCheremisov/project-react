from django.core.validators import MinValueValidator
from django.db import models

from foodgram import constants
from tags.models import Tag
from users.models import CustomUser


class Ingredient(models.Model):
    """Модель ингредиетов."""
    id = models.AutoField(primary_key=True)
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
    id = models.AutoField(primary_key=True)
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
        help_text='Загрузите изображение'
    )
    text = models.TextField(
        null=True,
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
        null=True,
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
        ordering = ['id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe'
            )
        ]

    def __str__(self):
        return f'{self.name} - автор: {self.author.username}'


class IngredientRecipes(models.Model):
    """Промежуточная модель с ингредиентами для рецепта."""
    id = models.AutoField(primary_key=True)
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(1,
                              'Минимальное количество ингредиентов'),
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


class Follow(models.Model):
    """Модель подписки на авторов."""

    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='follower'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                name='user_is_not_author',
                check=~models.Q(user=models.F('author'))
            )
        ]

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
