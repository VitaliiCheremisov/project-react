# Generated by Django 3.2.3 on 2023-12-25 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('favorite', '0001_initial'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]