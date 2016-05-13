from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.db import models as normal_models

from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError

from urllib2 import URLError


class Seller(normal_models.Model):
	name = normal_models.CharField(max_length=200)
	address = normal_models.CharField(max_length=100)
	location = models.PointField(u"longitude/latitude", geography=True, blank=True, null=True)
	phone = normal_models.IntegerField(blank=True, null=True)
	email = normal_models.CharField(max_length=50, blank=True, null=True)
	radius = normal_models.FloatField(default=10)
	open_hour = normal_models.IntegerField(blank=True, null=True)
	close_hour = normal_models.IntegerField(blank=True, null=True)
	item = normal_models.CharField(max_length=50, blank=True, null=True)
	item_unit = normal_models.CharField(max_length=50, blank=True, null=True)
	price_unit = normal_models.CharField(max_length=50, blank=True, null=True)
	picture = normal_models.FileField(blank=True, null=True)
	description = normal_models.TextField(blank=True, null=True)
	min_order_amount = normal_models.IntegerField(blank=True, null=True)
	license = normal_models.TextField(blank=True, null=True)
	license_exp = normal_models.DateField(blank=True, null=True)
	is_active = normal_models.BooleanField(default=True)
	operating_days = normal_models.CharField(max_length=100, blank=True, null=True)

	gis = models.GeoManager()
	objects = normal_models.Manager()

	def __unicode__(self):
	    return self.name

	def save(self, **kwargs):
		if not self.location:
			address = self.address.encode('utf-8')
			geocoder = GoogleV3()
			try:
				_, latlon = geocoder.geocode(address)
			except (URLError, GeocoderQueryError, ValueError, TypeError):
				print('Error')
			else:
				point = "POINT(%s %s)" % (latlon[1], latlon[0])
				self.location = geos.fromstr(point)

		super(Seller, self).save()        