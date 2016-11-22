from django.conf.urls import patterns, url

from kitchen import views

urlpatterns = patterns('kitchen.views',
    #url(r'transaction/$', views.TransactionList.as_view()),
    url(r'^$',                      views.home,  name="home"),
    url(r'tree/$',                  views.tree,  name="tree"),
    url(r'item/$',                  views.ItemList.as_view()),
    url(r'inventory/$',             views.inventory,         name='inventory'),
    url(r'shoppinglist/$',          views.shoppinglist_view, name='shoppinglist'),
    url(r'recipe_list/$',           views.recipe_list,       name='recipe_list'),
    url(r'recipe_add/$',            views.recipe_add,        name='recipe_add'),
    url(r'create_recipe/$',         views.create_recipe,       name='create_recipe'),
    url(r'recipeorder_list/$',      views.recipeorder_list,    name='recipeorder_list'),
    url(r'ingredient_add',          views.ingredient_add,      name='ingredient_add'),
    url(r'ingredient_create',       views.ingredient_create,   name='ingredient_create'),
    url(r'^(?P<ing_id>\d+)/ing_delete', views.ing_delete,           name='ing_delete'),
    url(r'item_selector/$',         views.item_selector,       name='item_selector'),
    url(r'item_selector_final/$',   views.item_selector_final, name='item_selector_final'),
    url(r'item_selector_test/$',    views.item_selector_test,  name='item_selector_test'),
    url(r'^(?P<recipe_id>\d+)/create_recipe_order/$',   views.create_recipe_order, name='create_recipe_order'),
    url(r'^(?P<recipe_id>\d+)/recipe_edit/$',           views.recipe_edit,         name='recipe_edit'),
    url(r'^(?P<recipeorder_id>\d+)/recipeorder_edit/$',     views.recipeorder_edit,    name='recipeorder_edit'),
    url(r'^(?P<recipeorder_id>\d+)/recipeorder_cancel/$',   views.recipeorder_cancel,   name='recipeorder_cancel'),
    url(r'^(?P<store_id>\d+)/store_edit/$',                 views.store_edit,          name='store_edit'),
    )

