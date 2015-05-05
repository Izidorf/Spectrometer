from django.conf.urls import patterns, url

from processing import views

urlpatterns = patterns('',
    url(r'^$', views.processUnknown, name='index'),
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^list/$', views.list, name='list'),
    url(r'^report/$', views.report, name='report'),
    url(r'^list/(?P<specter_id>\d+)/$', views.analyseSpecter, name='analyseSpecter'),
    url(r'^list/a/(?P<specter_id>\d+)/$', views.compareSpecter, name='compareSpecter'),
     # url(r'^list/(?P<question_id>\d+)/$', views.list, name='list'),compareSpecter
)