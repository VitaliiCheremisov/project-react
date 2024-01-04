from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from foodgram import constants


class CustomUser(AbstractUser):
    """Собственная модель пользоателя."""
    email = models.EmailField(
        max_length=constants.MAX_EMAIL_LENGTH,
        unique=True
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

    def clean_username(self):
        """Проверка на создание пользователя с username 'me'."""
        disallowed_usernames = ['me']
        if self.username.lower() in disallowed_usernames:
            raise ValidationError(
                'Имя пользователя "me" запрещено.'
            )

    def __str__(self):
        return f'{self.username} - {self.email}'
