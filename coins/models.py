import os

from decimal import Decimal
from django.db import models
from coins.thumbnails import ThumbnailImageField


class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=32, unique=True)
    genitive = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return self.name


def coins_path(coin, filename):
    country_name = coin.country.code
    nominal_name = {
        '2.00': '2e',
        '1.00': '1e',
        '0.50': '50c',
        '0.20': '20c',
        '0.10': '10c',
        '0.05': '5c',
        '0.02': '2c',
        '0.01': '1c'
    }["%.2f" % coin.nominal_value]
    extension = os.path.splitext(filename)[-1]
    return "coins/%s_%s%s" % (country_name, nominal_name, extension)


class Coin(models.Model):
    NOMINAL_VALUE_CHOICES = (
        (Decimal('2'), '2.00'),
        (Decimal('1'), '1.00'),
        (Decimal('0.5'), '0.50'),
        (Decimal('0.2'), '0.20'),
        (Decimal('0.1'), '0.10'),
        (Decimal('0.05'), '0.05'),
        (Decimal('0.02'), '0.02'),
        (Decimal('0.01'), '0.01'),
    )
    
    country = models.ForeignKey(Country)
    
    nominal_value = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        choices = NOMINAL_VALUE_CHOICES)
    
    image = ThumbnailImageField(
        upload_to=coins_path,
        sizes=((100,100),),
        max_length=255)
    
    commemorative_year = models.IntegerField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    collected_by = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "%s | %.2f" % (self.country.name, self.nominal_value)
