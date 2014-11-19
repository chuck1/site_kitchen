from django.db import models

# Create your models here.

class Unit(models.Model):
    name = models.CharField(max_length=256)
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
    def __unicode__(self):
        return self.recipe.name




