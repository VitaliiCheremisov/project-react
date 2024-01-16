from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from foodgram import constants


class CustomUser(AbstractUser):
    """Собственная модель пользоателя."""
    email = models.EmailField(
        max_length=constants.MAX_EMAIL_LENGTH,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        max_length=constants.MAX_NAME_LENGTH,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=constants.MAX_NAME_LENGTH,
        verbose_name='Фамилия'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_and_email'
            )
        ]

    def __str__(self):
        return f'{self.username} - {self.email}'

    def clean(self):
        """Проверка на создание пользователя с username 'me'."""
        if self.username.lower() in settings.DISALLOWED_USERNAMES:
            raise ValidationError(
                'Имя пользователя "me" запрещено.'
            )
