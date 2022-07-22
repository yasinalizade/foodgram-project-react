from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth.models import AnonymousUser
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError

from ingredients.models import Ingredient
from recipes.models import (Favorite, Tag, Recipe,
                            IngredientRecipe, Shopping, TagRecipe)
from users.models import Subscription

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'email', 'password',
                  'username', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if isinstance(user, AnonymousUser):
            return False
        return Subscription.objects.filter(user=user, author=obj).exists()


class IngredientRecipeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')

    def get_name(self, obj):
        return obj.name

    def get_measurement_unit(self, obj):
        return obj.measurement_unit


class IngredientsField(serializers.Field):
    def to_representation(self, value):
        serializer = IngredientRecipeSerializer(value, many=True)
        return serializer.data

    def to_internal_value(self, data):
        return data


class TagsField(serializers.Field):
    def to_representation(self, value):
        tags = []
        serializer = TagSerializer(value, many=True)
        for elem in serializer.data:
            tags.append(elem['id'])
        return tags

    def to_internal_value(self, data):
        return data


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientsField()
    tags = TagsField()
    author = CustomUserSerializer(read_only=True, required=False)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author',
                  'text', 'tags', 'ingredients', 'cooking_time',
                  'image', 'is_in_shopping_cart', 'is_favorited')

    def validate_tags(self, value):
        if len(value) == 0:
            raise ValidationError('Tag list cannot be empty!')
        for elem in value:
            tags = Tag.objects.filter(pk=elem)
            if tags.count() == 0:
                raise ValidationError(f'Tag with {elem} does not exist')
        return value

    def validate_ingredients(self, value):
        if len(value) == 0:
            raise ValidationError('Ingredient list cannot be empty!')
        for elem in value:
            pk = elem.get('id', None)
            if pk is None:
                raise ValidationError('Check ingredients id')
            ingredients = Ingredient.objects.filter(pk=pk)
            if ingredients.count() == 0:
                raise ValidationError(f'Ingredient with {pk} does not exist!')
        return value

    def add_tags(self, recipe, tags):
        links = []
        for pk in tags:
            obj = Tag.objects.get(pk=pk)
            links.append(TagRecipe(recipe=recipe, tag=obj))
        TagRecipe.objects.bulk_create(links)

    def add_ingredients(self, recipe, ingredients):
        links = []
        for ingredient in ingredients:
            obj = Ingredient.objects.get(pk=ingredient.get('id'))
            links.append(IngredientRecipe(
                recipe=recipe,
                ingredient=obj,
                amount=ingredient.get('amount')
            ))
        IngredientRecipe.objects.bulk_create(links)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        request = self.context.get('request')
        recipe = Recipe.objects.create(author=request.user,
                                       **validated_data)

        self.add_tags(recipe, tags)
        self.add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        validation = ['name', 'image',
                      'text', 'cooking_time']

        for elem in validation:
            val = validated_data.get(elem)
            setattr(instance, elem, val)

        TagRecipe.objects.filter(recipe=instance).delete()
        self.add_tags(instance, tags)

        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.add_ingredients(instance, ingredients)

        instance.save()
        return instance

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if isinstance(user, AnonymousUser):
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        if isinstance(user, AnonymousUser):
            return False
        return Shopping.objects.filter(user=user, recipe=obj).exists()


class ShortRecipeSerializer(RecipeSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return ShortRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
