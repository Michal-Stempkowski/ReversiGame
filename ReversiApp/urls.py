from django.conf.urls import patterns, url

from ReversiApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'new/$', views.new_game, name='new_game'),
    url(r'new/creation_result/$', views.new_game_creation_result, name='new_game_creation_result'),
    url(r'load/$', views.load_game, name='load_game'),
    # url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)