from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from ingredients.models import Ingredient

User = get_user_model()


class Tag(models.Model):
    """Model describes tags."""

    name = models.CharField(
        _('Name'),
        max_length=200,
        db_index=True,
        blank=False,
        unique=True
    )
    color = models.CharField(
        _('Color'),
        max_length=7,
        blank=False,
        unique=True
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=200,
        blank=False,
        unique=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self) -> str:
        return f'{self.name}'


class Recipe(models.Model):
    """Model describes recipes with text, images, tags and ingredients."""

    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes_ingredients',
        verbose_name='Ingredients',
        through='IngredientRecipe'
        )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Tags',
        through='TagRecipe'
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name=_('User')
        )
    image = models.ImageField(upload_to='media/', null=False, blank=False)
    name = models.CharField(_('Name'), max_length=200, db_index=True, blank=False)
    text = models.TextField(_('Description'))
    shopping_cart = models.ManyToManyField(
        User,
        related_name='recipes_shopping',
        verbose_name=_('Shopping_cart'),
        through='Shopping'
    )
    favorite = models.ManyToManyField(
        User,
        related_name='recipes_favorite',
        verbose_name=_('Favorite'),
        through='Favorite',
    )
    cooking_time = models.PositiveSmallIntegerField(
        _('Cooking time'),
        help_text='in minutes',
        blank=False
        )
    pub_date = models.DateTimeField(_('Publication date'), auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    def __str__(self) -> str:
        return f'{self.name}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_tag'
    )


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        blank=False
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        blank=False
    )
    amount = models.PositiveSmallIntegerField(
        _('Amount'),
        default=1,
        null=False,
        blank=False,
    )


class Shopping(models.Model):
    """
    User can add recipe and its ingredients to the shopping cart.
    It is possible to create pdf-file with list of ingredients.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name=_('Customer'),
        db_index=True
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name=_('Recipe')
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique cart user')
        ]

    def __str__(self):
        return f'{self.recipe} in {self.user}\'s cart'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('Customer'),
        db_index=True
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('Recipe')
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='favorite recipe for unique user')
        ]

    def __str__(self):
        return f'{self.user} liked this {self.recipe}'
