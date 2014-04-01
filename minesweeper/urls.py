from django.conf.urls import patterns, include, url
import profiles

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'minesweeper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$register/', 'profiles.views.current_datetime', name='register'),
)
