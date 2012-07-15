from django.core.urlresolvers import reverse
from django.http import HttpResponse
from coins.models import Coin, Country

def index(request):
    countries = Country.objects.all().order_by('name')
    output = '<br />'.join(['<a href="%s">%s</a>' % (reverse(country, args=[c.code]), c) for c in countries])
    return HttpResponse("<h1>Country list</h1><p>%s</p>" % output)

def country(request, country_code):
    coins = Coin.objects.filter(country__code=country_code)
    output = '<br />'.join(['<img src="%s" />' % c.small_image_url for c in coins])
    return HttpResponse("<h1>Looking at coins from %s</h1><p>%s</p>" % (country_code, output))
