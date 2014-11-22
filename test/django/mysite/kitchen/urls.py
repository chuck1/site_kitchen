from django.conf.urls import patterns, url

from kitchen import views

urlpatterns = patterns('kitchen.views',
    #url(r'transaction/$', views.TransactionList.as_view()),
    url(r'item/$', views.ItemList.as_view()),
    url(r'inventory/$', views.inventory, name='inventory_view'),
    url(r'shoppinglist/$', views.shoppinglist_view, name='shoppinglist_view'),
    url(r'^(?P<recipe_id>\d+)/create_recipe_order/$', views.create_recipe_order, name='create_recipe_order'),
    )

