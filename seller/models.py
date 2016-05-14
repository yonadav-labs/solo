from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis import geos

from django.db import models as normal_models

from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError

from urllib2 import URLError


PRICE_UNIT = (
	('Dollar', 'Dollar'),
	('Cent', 'Cent'),
)


class Seller(normal_models.Model):
	name = normal_models.CharField(max_length=200)
	address = normal_models.CharField(max_length=100)
	location = models.PointField(u"longitude/latitude", geography=True, blank=True, null=True)
	phone = normal_models.IntegerField(blank=True, null=True)
	email = normal_models.CharField(max_length=50)
	radius = normal_models.FloatField(default=10)
	open_hour = normal_models.IntegerField(default=8)
	close_hour = normal_models.IntegerField(default=6)

	item = normal_models.CharField(max_length=50)
	item_unit = normal_models.CharField(max_length=50, blank=True, null=True)
	price_unit = normal_models.CharField(choices=PRICE_UNIT, max_length=50, blank=True, null=True)
	picture = normal_models.FileField(blank=True, null=True)
	description = normal_models.TextField(blank=True, null=True)
	min_order_amount = normal_models.IntegerField(default=1)
	license_number = normal_models.CharField(max_length=50, default='234523525342')
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


class Order(normal_models.Model):
	owner = models.ForeignKey(Seller, related_name="orders")
	# pickup_addr = models.CharField(max_length=250)
	# dropoff_addr = models.CharField(max_length=250)
	# contact_name = models.CharField(max_length=250)
	# phone = models.CharField(max_length=20)
	# pickup_time = models.DateTimeField()
	# dropoff_time = models.DateTimeField(blank=True, null=True, default='')
	# items = models.CharField(choices=ITEMS, max_length=50)
	# payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=50)
	# key = models.CharField(max_length=100)
	# status = models.CharField(choices=STATUS, default='Initial', max_length=20)
	# track_link = models.CharField(max_length=200, blank=True, null=True)
	quantity = normal_models.FloatField()


	def __str__(self):
		return self.owner.username
