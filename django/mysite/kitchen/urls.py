from django.conf.urls import patterns, url

from kitchen import views

urlpatterns = patterns('kitchen.views',
    #url(r'transaction/$', views.TransactionList.as_view()),
    url(r'^$',             views.index, name="index"),
    url(r'item/$',         views.ItemList.as_view()),
    url(r'inventory/$',    views.inventory, name='inventory_view'),
    url(r'shoppinglist/$', views.shoppinglist_view, name='shoppinglist_view'),
    url(r'add_recipe/$',   views.add_recipe, name='add_recipe'),
    url(r'^(?P<recipe_id>\d+)/create_recipe_order/$', views.create_recipe_order, name='create_recipe_order'),
    url(r'create_recipe/$', views.create_recipe, name='create_recipe'),
    )

