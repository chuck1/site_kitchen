from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse

from recipe.models import Recipe
from recipe.models import Ingredient

def index(request):
	return HttpResponse("Hello, world")

def detail(request, recipe_id):
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	ing = Ingredient.objects.all() #filter(recipe_id=recipe_id)
	context = {'ingredients':ing}
	return render(request, 'recipe/detail.html', context)


