from django.contrib import admin

# Register your models here.

from recipe.models import Recipe
from recipe.models import Item
from recipe.models import Ingredient

admin.site.register(Recipe)
admin.site.register(Item)
admin.site.register(Ingredient)

