from django.conf.urls import patterns, url

urlpatterns = patterns('coins.views',
    url(r'^$', 'index'),
    url(r'^(?P<country_code>[a-z]{2})/$', 'country'),
    url(r'^(?P<year>\d{4})/$', 'commemorative'),
    url(r'^(?P<value>2\.00|1\.00|0\.50|0\.20|0\.10|0\.05|0\.02|0\.01)/$', 'nominal'),
)
