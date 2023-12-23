from django.db import models
from foodgram import constants


class Tag(models.Model):
    """Модель для тэгов."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=constants.MAX_TAG_NAME_LENGTH,
        verbose_name='Название тэга'
    )
    color = models.CharField(
        max_length=constants.MAX_COLOR_LENGTH,
        verbose_name='Цвет',
        unique=True
    )
    slug = models.SlugField(
        max_length=constants.MAX_SLUG_LENGTH,
        verbose_name='Слаг',
        unique=True
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name
