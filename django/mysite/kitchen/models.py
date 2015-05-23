from django.db import models

# Create your models here.

class MeasurementType(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=256)
    measurementtype = models.ForeignKey(MeasurementType)
    
    convert = models.FloatField(null=True)
    
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name   = models.CharField(max_length=256)
    #parent = models.ForeignKey(Category, null=True)

    def __unicode__(self):
        return self.name

class Item(models.Model):

    CATEGORY_CHOICES = (
            ('baking',  'baking'),
            ('bulk',    'bulk'),
            ('cheese',  'cheese'),
            ('dairy',   'dairy'),
            ('meat',    'meat'),
            ('produce', 'produce'),
            ('unknown', 'unknown'),
            )

    name = models.CharField(max_length=256)
    unit = models.ForeignKey(Unit, null=True)
    category = models.CharField(max_length=128, choices=CATEGORY_CHOICES)
    
    category2 = models.ForeignKey(Category, null=True)

    def __unicode__(self):
        #return "Item:" + self.name
        return self.name

    class Meta:
        ordering = ('name',)

class Recipe(models.Model):
    name = models.CharField(max_length=256)
    source = models.CharField(max_length=256, blank=True)
    lcm = models.FloatField(default=1.0)
    ingredients = models.ManyToManyField(Item, through='Ingredient')
    text = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return "Recipe:" + self.name
    def can_make(self, a, ir_dict):
        #print("can_make")
        #print(ir_dict)

        ings = Ingredient.objects.filter(recipe=self, amount__gt=0)
        
        #print(ings)

        for ing in ings:
            need = a * ing.amount_std

            if not ing.item in ir_dict:
                if need > 0:
                    return False

            ir = ir_dict[ing.item]
            
            if ir < need:
                return False

        return True

class RecipeOrder(models.Model):
    recipe = models.ForeignKey(Recipe)
    amount = models.FloatField()
    def __unicode__(self):
        return self.recipe.name + ": " + str(self.amount)

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    item = models.ForeignKey(Item)
    unit = models.ForeignKey(Unit)
    amount = models.FloatField()
    optional = models.BooleanField(default=False)
    def __unicode__(self):
        return self.recipe.name + ": " + self.item.name
    def _get_amount_std(self):
        return self.amount * self.unit.convert
    amount_std = property(_get_amount_std)
    
class Transaction(models.Model):
    item = models.ForeignKey(Item)
    unit = models.ForeignKey(Unit)
    amount = models.FloatField()
    def __unicode__(self):
        return self.item.name + ":" + str(self.amount_std)
    def _get_amount_std(self):
        return self.amount * self.unit.convert
    amount_std = property(_get_amount_std)







