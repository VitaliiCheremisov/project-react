# Generated by Django 3.2.3 on 2024-01-15 11:28

import colorfield.fields
from django.db import migrations
import tags.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=7, samples=None, unique=True, validators=[tags.validators.hex_color_validator], verbose_name='Цвет'),
        ),
    ]
