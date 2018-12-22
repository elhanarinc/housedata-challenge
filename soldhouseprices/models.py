from django.db import models
from postgres_copy import CopyManager


class HouseData(models.Model):
    transaction_unique_identifier = models.CharField(primary_key=True, max_length=50)
    price = models.IntegerField()
    date_of_transfer = models.DateTimeField()
    postcode = models.CharField(max_length=200)
    property_type = models.CharField(max_length=1)
    old_or_new = models.CharField(max_length=1)
    duration = models.CharField(max_length=1)
    paon = models.CharField(max_length=50)
    saon = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    locality = models.CharField(max_length=50, blank=True)
    town = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    ppd_category_type = models.CharField(max_length=1)
    record_status = models.CharField(max_length=1)
    copy_objects = CopyManager()
    objects = models.Manager()
