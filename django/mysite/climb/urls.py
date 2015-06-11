from django.conf.urls import patterns, url

from climb import views

urlpatterns = patterns('kitchen.views',
    url(r'^$',                    views.index,           name="index"),
    url(r'route_create/$',        views.route_create,    name='route_create'),
    )

