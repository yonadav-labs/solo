from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models as normal_models
from django.conf import settings
 
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError

from urllib2 import URLError


Estimated_Order_to_Delivery = (
	(1, '1 hour'),
	(2, 'Same Day'),
	(3, 'Next Day'),
	(4, 'Please Contact'),
	(5, 'Unknown')
	)


class WeekDay(normal_models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Seller(AbstractUser):
	address = normal_models.CharField(max_length=100)
	location = models.PointField(u"longitude/latitude", geography=True, blank=True, null=True)
	phone = models.CharField(max_length=20, null=True, blank=True) # validators should be a list
	radius = normal_models.FloatField(default=10)	# in miles
	open_hour = normal_models.TimeField(default='08:00:00')
	close_hour = normal_models.TimeField(default='18:30:00') #?? What if they are open from midnight to 3 am? How do we allow them to have hours between days? Also, how about if they have different hours for different days? Thoughts?
	item = normal_models.CharField(max_length=50)
	unit_price = normal_models.DecimalField(blank=True, null=False, default=00.00, decimal_places=2, max_digits=6 ) # price in cents
	min_order = normal_models.DecimalField(default=1.00, decimal_places=2, max_digits=6) # unit_price multiplied by min_order_amount 
	picture = normal_models.FileField(blank=True, null=True)
	description = normal_models.TextField(blank=True, null=True)
	min_order_amount = normal_models.IntegerField(default=1)
	permit_number = normal_models.CharField(max_length=50, default='234523525342')
	license = normal_models.TextField(blank=True, null=True)
	permit_exp = normal_models.DateField(blank=True, null=True)
	estimated_delivery = normal_models.IntegerField(choices=Estimated_Order_to_Delivery, default=1)
	operating_days = normal_models.ManyToManyField(WeekDay, related_name='operating_days')

	objects = UserManager()
	gis = models.GeoManager()

	def __unicode__(self):
		return self.username

	def save(self, **kwargs):
		min_order = self.unit_price * self.min_order_amount * 100
		address = self.address.encode('utf-8')
		geocoder = GoogleV3()
		try:
			_, latlon = geocoder.geocode(address)
		except (URLError, GeocoderQueryError, ValueError, TypeError):
			latlon = ['0', '0']
		finally:
			point = "POINT(%s %s)" % (latlon[1], latlon[0])
			self.location = geos.fromstr(point)

		super(Seller, self).save()        

		

class Sale(normal_models.Model):
	seller = normal_models.ForeignKey(Seller, related_name='seller')
	quantity = normal_models.FloatField()
	charge_id = normal_models.CharField(max_length=32, null=True, blank=True) # this should be returned with the Strip Connect api redirect json
	delivery_address = normal_models.CharField(max_length=500)
	buyer_name = normal_models.CharField(max_length=50)
	buyer_phone = normal_models.CharField(max_length=20)

	def __unicode__(self):
		return self.seller.name + ':' + self.buyer_name
	