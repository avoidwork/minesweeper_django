from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^games/recent/', 'games.views.recently_completed'),
    url(r'^games/(?P<game_id>\d+)/', 'games.views.details'),
    url(r'^games/(?P<game_id>\d+)/move/', 'games.views.move'),
    url(r'^games/(?P<game_id>\d+)/moves/', 'games.views.moves'),
    url(r'^register/', 'profiles.views.current_datetime'),
    url(r'^login/', 'profiles.views.current_datetime'),
    url(r'^admin/', include(admin.site.urls)),
)