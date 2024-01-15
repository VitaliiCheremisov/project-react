from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

CustomUser = get_user_model()


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
            )
        ]

    def clean(self):
        """Проверка на самоподписку."""
        if self.author == self.user:
            raise ValidationError(
                'Нельзя подписаться на самого себя.'

            )

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
