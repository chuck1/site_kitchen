from django.db import models

# Create your models here.

class MeasurementType(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=256)
    measurementtype = models.ForeignKey(MeasurementType)
    def __unicode__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return self.name

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    item = models.ForeignKey(Item)
    unit = models.ForeignKey(Unit)
    amount = models.FloatField()
    def __unicode__(self):
        return self.recipe.name

class Transaction(models.Model):
    item = models.ForeignKey(Item)
    unit = models.ForeignKey(Unit)
    amount = models.FloatField()
   


