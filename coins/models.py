# -*- encoding: utf-8 -*-

import os

from decimal import Decimal
from django.db import models
from coins.fields import CurrencyField, ThumbnailedImageField


class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=32, unique=True)
    genitive = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def _get_common_coins(self):
        return Coin.objects.filter(country=self, commemorative_year=None).order_by('nominal_value')
    common_coins = property(_get_common_coins)

    def _get_commemorative_coins(self):
        return Coin.objects.filter(country=self, commemorative_year__isnull=False).order_by('commemorative_year')
    commemorative_coins = property(_get_commemorative_coins)

    def _get_collected_count(self):
        return Coin.objects.filter(country=self, collected_at__isnull=False).count()
    collected_count = property(_get_collected_count)

    def _get_total_count(self):
        return Coin.objects.filter(country=self).count()
    total_count = property(_get_total_count)


def coins_path(coin, filename):
    country_name = coin.country.code
    extension = os.path.splitext(filename)[-1]
    if coin.commemorative_year:
        return 'coins/%s_%d%s' % (country_name, coin.commemorative_year, extension)
    return 'coins/%s_%s%s' % (country_name, coin.short_name, extension)


class Coin(models.Model):
    NOMINAL_VALUE_CHOICES = (
        (Decimal('2.00'), '€2.00'),
        (Decimal('1.00'), '€1.00'),
        (Decimal('0.50'), '€0.50'),
        (Decimal('0.20'), '€0.20'),
        (Decimal('0.10'), '€0.10'),
        (Decimal('0.05'), '€0.05'),
        (Decimal('0.02'), '€0.02'),
        (Decimal('0.01'), '€0.01'),
    )

    country = models.ForeignKey(Country)

    nominal_value = CurrencyField(
        max_digits=3,
        decimal_places=2,
        choices=NOMINAL_VALUE_CHOICES)

    image = ThumbnailedImageField(upload_to=coins_path, watermark='watermark.png', max_length=255)
    commemorative_year = models.IntegerField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    collected_by = models.CharField(max_length=255, null=True, blank=True)

    def _get_short_name(self):
        nominal_str = str(self.nominal_value)
        if nominal_str.endswith('.00'):
            return '%se' % nominal_str[0]
        if nominal_str.endswith('0'):
            return '%s0c' % nominal_str[2]
        return '%sc' % nominal_str[3]
    short_name = property(_get_short_name)

    def __unicode__(self):
        if self.commemorative_year:
            return u"%s comm. %d" % (self.country.genitive, self.commemorative_year)
        return u"%s €%s" % (self.country.genitive, self.nominal_value)

    def _get_image_url(self):
        if self.collected_at:
            return self.image.url_collected
        return self.image.url_thumb
    image_url = property(_get_image_url)

    @staticmethod
    def get_commemorative_year_list():
        query_set = Coin.objects.values_list('commemorative_year').filter(commemorative_year__isnull=False).order_by('-commemorative_year')
        query_set.query.group_by = []
        return [row[0] for row in query_set]
