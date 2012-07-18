from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from coins.models import Coin, Country
from datetime import datetime


def _update_general_context(request, context=None):
    parameters = {
        'countries': Country.objects.all().order_by('name'),
        'commemorative_years': Coin.get_commemorative_year_list(),
        'nominal_values': [str(value[0]) for value in Coin.NOMINAL_VALUE_CHOICES],
    }
    return RequestContext(request, parameters) if not context else context.update(parameters)


def index(request):
    context = _update_general_context(request)
    return render_to_response(
        'coins/index.html',
        {},
        context_instance=context)


def country(request, country_code):
    context = _update_general_context(request)
    return render_to_response(
        'coins/country.html',
        {
            'country': get_object_or_404(Country, code=country_code),
        },
        context_instance=context)


def commemorative(request, year):
    year = int(year)
    if year < 2004 or year > datetime.now().year:
        raise Http404
    context = _update_general_context(request)
    return render_to_response(
        'coins/commemorative.html',
        {
            'year': year,
            'coins': Coin.objects.filter(commemorative_year=year).order_by('country__name'),
        },
        context_instance=context)


def nominal(request, value):
    context = _update_general_context(request)
    return render_to_response(
        'coins/nominal.html',
        {
            'nominal_value': value,
            'coins': Coin.objects.filter(nominal_value=value, commemorative_year=None).order_by('country__name'),
        },
        context_instance=context)
