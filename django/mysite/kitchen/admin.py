from django.contrib import admin

# Register your models here.

from kitchen.models import MeasurementType
from kitchen.models import Unit
from kitchen.models import Item
from kitchen.models import Recipe
from kitchen.models import RecipeOrder
from kitchen.models import Ingredient
from kitchen.models import Transaction

import kitchen.models

admin.site.register(MeasurementType)
admin.site.register(Unit)
#admin.site.register(Item)
#admin.site.register(Recipe)
admin.site.register(RecipeOrder)
admin.site.register(Ingredient)
admin.site.register(Transaction)
admin.site.register(kitchen.models.Category)



class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)

class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)


admin.site.register(Item, ItemAdmin)
admin.site.register(Recipe, RecipeAdmin)



