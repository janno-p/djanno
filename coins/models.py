from django.db import models


class NominalValue(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.value


class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=32, unique=True)
    genitive = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return self.name


class Coin(models.Model):
    country = models.ForeignKey(Country)
    nominal_value = models.ForeignKey(NominalValue)
    commemorative_year = models.IntegerField(null=True)
    image_file_name = models.CharField(max_length=255)
    image_content_type = models.CharField(max_length=255)
    image_file_size = models.IntegerField()
    collected_at = models.DateTimeField(null=True)
    collected_by = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return "%s | %s" % (self.country.name, self.nominal_value.value)
