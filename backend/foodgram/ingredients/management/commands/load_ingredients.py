from csv import DictReader

from django.core.management import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Show this if the data already exist in the database
        if Ingredient.objects.count() > 0:
            print('all data already loaded...exiting.')
            return
        # Show this before loading the data into the database
        print('Loading ingredients...')
        # Code to load the data into database
        for row in DictReader(open(
                '../../data/ingredients.csv', encoding='utf-8')):
            ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row[' measurement_unit'],
            )
            ingredient.save()
        print('...done')
