from django.conf.urls import patterns, url

from kitchen import views

urlpatterns = patterns('',
    url(r'transaction/$', views.TransactionList.as_view()),
    url(r'inventory/$', views.inventory, name='inventory'),
    )

