# Generated by Django 3.2.3 on 2024-01-12 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_delete_follow'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_data', 'id'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
    ]