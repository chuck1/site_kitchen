import django.forms

class add_recipe(django.forms.Form):
    name   = django.forms.CharField(max_length=256)
    source = django.forms.CharField(max_length=256)
    lcm    = django.forms.FloatField()
    #ingredients = models.ManyToManyField(Item, through='Ingredient')
    #text   = django.forms.TextField()


