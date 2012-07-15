from django.conf.urls import patterns, url

urlpatterns = patterns('coins.views',
    url(r'^$', 'index'),
    url(r'^(?P<country_code>[a-z]{2})/$', 'country'),
    #url(r'^(?P<coin_id>\d+)/results/$', 'results'),
    #url(r'^(?P<coin_id>\d+)/vote/$', 'vote'),
)
