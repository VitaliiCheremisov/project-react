from django.contrib.auth.models import AbstractUser
from django.db import models
from foodgram import constants


class CustomUser(AbstractUser):
    """Собственная модель пользоателя."""
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        blank=False,
        null=False,
        max_length=constants.MAX_EMAIL_LENGTH,
        unique=True
    )

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
        return self.username
