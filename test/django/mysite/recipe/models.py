from django.db import models

# Create your models here.

class Recipe(models.Model):
	recipe_name = models.CharField(max_length=200)
	receip_text = models.CharField(max_length=1000)
	def __unicode__(self):
		return self.recipe_name

class Item(models.Model):
	item_name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.item_name
	
class Ingredient(models.Model):
	recipe = models.ForeignKey(Recipe)
	item = models.ForeignKey(Item)
	unit = models.CharField(max_length=200)
	quantity = models.FloatField()
	def __unicode__(self):
		return self.recipe.recipe_name + ":" + self.item.item_name

