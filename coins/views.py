from django.shortcuts import get_object_or_404, render_to_response
from coins.models import Country

def index(request):
    countries = Country.objects.all().order_by('name')
    return render_to_response('coins/index.html', {
        'countries': countries
    })

def country(request, country_code):
    country = get_object_or_404(Country, code=country_code)
    return render_to_response('coins/country.html', {
        'country': country
    })
