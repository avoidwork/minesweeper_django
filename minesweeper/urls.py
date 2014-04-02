from django.shortcuts import redirect
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

import settings

def index(request):
    return redirect('/index.html');

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
    url(r'^games/$', 'games.views.index'),
    url(r'^games/new/$', 'games.views.new'),
    url(r'^games/(?P<game_id>\d+)/$', 'games.views.details'),
    url(r'^games/(?P<game_id>\d+)/move/$', 'games.views.move'),
    url(r'^$', index),
    url(r'^(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
)