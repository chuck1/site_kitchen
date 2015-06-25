from django.conf.urls import patterns, url

from jobdata import views

urlpatterns = patterns('kitchen.views',
    url(r'form_signup/$',        views.form_signup,  name="form_signup"),
    url(r'form_login/$',         views.form_login,   name="form_login"),
    )

