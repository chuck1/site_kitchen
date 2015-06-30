from django.conf.urls import patterns, url

from jobdata import views

urlpatterns = patterns('kitchen.views',
    
    url(r'form_signup/$',        views.form_signup,    name="form_signup"),
    url(r'form_login/$',         views.form_login,     name="form_login"),
    url(r'logout/$',             views.logout,         name="logout"),

    url(r'^$',                   views.json_editor,    name="json_editor"),
    url(r'json_editor/$',        views.json_editor,    name="json_editor"),

    url(r'resume_render/$',      views.resume_render,  name="resume_render"),
    url(r'json_render/$',        views.json_render,    name="json_render"),
    )

