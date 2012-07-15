import os

from decimal import Decimal
from django.db import models
from django_thumbs.db.models import ImageWithThumbsField


class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=32, unique=True)
    genitive = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return self.name


class Coin(models.Model):
    NOMINAL_VALUE_CHOICES = (
        (Decimal('2.00'), '2.00'),
        (Decimal('1.00'), '1.00'),
        (Decimal('0.50'), '0.50'),
        (Decimal('0.20'), '0.20'),
        (Decimal('0.10'), '0.10'),
        (Decimal('0.05'), '0.05'),
        (Decimal('0.02'), '0.02'),
        (Decimal('0.01'), '0.01'),
    )
    
    def coins_update_path(coin, filename):
        print("%s, %s" % (coin, filename))
        country_name = coin.country.code
        nominal_name = ("%.2f" % coin.nominal_value).replace('.', 'c')
        parts = os.path.splitext(filename)
        return "coins/%s_%s%s" % (country_name, nominal_name, parts[-1])
    
    country = models.ForeignKey(Country)
    
    nominal_value = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        choices = NOMINAL_VALUE_CHOICES)
    
    image = ImageWithThumbsField(
        upload_to=coins_update_path,
        sizes=((100,100),),
        max_length=255)
    
    commemorative_year = models.IntegerField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    collected_by = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "%s | %s" % (self.country.name, self.nominal_value)
