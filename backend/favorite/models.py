from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe

CustomUser = get_user_model()


class Favorite(models.Model):
    """Модель избранное."""
    user = models.ForeignKey(
        CustomUser,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'Избранные рецепты {self.user.username}'
