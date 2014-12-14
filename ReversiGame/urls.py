from django.conf.urls import patterns, include, url
from django.contrib import admin
import ReversiGame.views as views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ReversiGame.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^game2/', include(views.game)),
    url(r'^game/', include('ReversiApp.urls')),
)
