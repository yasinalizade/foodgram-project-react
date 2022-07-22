from django.core.management import BaseCommand
from ingredients.models import Ingredient
from recipes.models import IngredientRecipe


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Show this if the data already exist in the database
        if Ingredient.objects.count() == 0:
            print('There are no rows in the table')
            return
        print("Delete all data...")
        Ingredient.objects.all().delete()
        IngredientRecipe.objects.all().delete()
        print('...done')
