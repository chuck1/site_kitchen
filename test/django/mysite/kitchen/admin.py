from django.contrib import admin

# Register your models here.

from kitchen.models import MeasurementType
from kitchen.models import Unit
from kitchen.models import Item
from kitchen.models import Recipe
from kitchen.models import Ingredient
from kitchen.models import Transaction

admin.site.register(MeasurementType)
admin.site.register(Unit)
admin.site.register(Item)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Transaction)



