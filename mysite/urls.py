from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'kitchen.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^kitchen/',  include('kitchen.urls',  namespace="kitchen")),
    url(r'^admin/', include(admin.site.urls)),
)

