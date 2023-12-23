import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


def ingredient_create(row):
    print(row[0], row[1])
    Ingredient.objects.get_or_create(
        name=row[0],
        measurement_unit=row[1],
    )


action = {
    "ingredients.csv": ingredient_create,
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        for filename in options['filename']:
            path = os.path.join(settings.BASE_DIR, 'data/') + filename
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    action[filename](row)
