from django.conf.urls import patterns, url

from task import views

urlpatterns = patterns('task.views',
    url(r'^$', views.index, name='index'),
    url(r'tasklist/$',                    views.tasklist,      name='tasklist'),
    url(r'form_task_add/$',               views.form_task_add, name='form_task_add'),
    url(r'^(?P<task_id>\d+)/start_now/$', views.start_now,     name='start_now'),
    url(r'^(?P<task_id>\d+)/end_now/$',   views.end_now,       name='end_now'),
    )

