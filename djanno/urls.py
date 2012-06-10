from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djanno.views.home', name='home'),
    # url(r'^djanno/', include('djanno.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^coins/$', 'coins.views.index'),
    url(r'^coins/(?P<coin_id>\d+)/$', 'coins.views.detail'),
    url(r'^coins/(?P<coin_id>\d+)/results/$', 'coins.views.results'),
    url(r'^coins/(?P<coin_id>\d+)/vote/$', 'coins.views.vote'),
)
