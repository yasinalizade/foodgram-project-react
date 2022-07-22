from django.contrib import admin

from .models import Tag, TagRecipe, Recipe, IngredientRecipe


class TagsInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_filter = ('name', 'slug')
    empty_value_display = '--empty--'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    inlines = (TagsInline, IngredientInline)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '--empty--'


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
