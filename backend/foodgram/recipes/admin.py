from django.contrib import admin

from .models import IngredientAmount, Recipe, Tag, TagRecipe


class TagsInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class IngredientInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_filter = ('name', 'slug')
    empty_value_display = '--empty--'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    inlines = (TagsInline, IngredientInline)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '--empty--'
