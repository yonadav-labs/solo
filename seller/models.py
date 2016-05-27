from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models as normal_models
from django.conf import settings
 
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError

from urllib2 import URLError

# for phone number validator
from django.core.validators import RegexValidator # source: http://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models


class Seller(AbstractUser):
	address = normal_models.CharField(max_length=100)
	location = models.PointField(u"longitude/latitude", geography=True, blank=True, null=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone = models.CharField(max_length=12 ,validators=[phone_regex], blank=True) # validators should be a list
	radius = normal_models.FloatField(default=10)	# in miles
	open_hour = normal_models.IntegerField(default=8)
	close_hour = normal_models.IntegerField(default=6)
	item = normal_models.CharField(max_length=50)
	unit_price = normal_models.IntegerField(blank=True, null=True)		# price in cent
	picture = normal_models.FileField(blank=True, null=True)
	description = normal_models.TextField(blank=True, null=True)
	min_order_amount = normal_models.IntegerField(default=1)
	permit_number = normal_models.CharField(max_length=50, default='234523525342')
	license = normal_models.TextField(blank=True, null=True)
	permit_exp = normal_models.DateField(blank=True, null=True)
	operating_days = normal_models.CharField(max_length=100, blank=True, null=True) # how does this work? How do we select M-F and times for each day. How does Seller go on vacation and take a break or set status to "on-hold" for a period of time? How do we use this to show sellers to customers when they query based on location etc.?

	objects = UserManager()
	gis = models.GeoManager()

	def __unicode__(self):
		return self.username

	def save(self, **kwargs):
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

# open hours 
# reference: http://stackoverflow.com/questions/12216771/django-objects-for-business-hours
WEEKDAYS = [
  (1, ("Monday")),
  (2, ("Tuesday")),
  (3, ("Wednesday")),
  (4, ("Thursday")),
  (5, ("Friday")),
  (6, ("Saturday")),
  (7, ("Sunday")),
]


class OpeningHours(models.Model):
	store = models.ForeignKey(Seller)
	weekday = models.IntegerField(
        choices=WEEKDAYS,
        unique=True )
	from_hour = models.TimeField()
	to_hour = models.DurationField()
	
	class Meta:
		unique_together=(('weekday', 'store',),)
		

class Sale(normal_models.Model):
	seller = normal_models.ForeignKey(Seller, related_name='seller')
	quantity = normal_models.FloatField()
	charge_id = normal_models.CharField(max_length=32, null=True, blank=True) # this should be returned with the Strip Connect api redirect json
	delivery_address = normal_models.CharField(max_length=500)
	buyer_name = normal_models.CharField(max_length=50)
	buyer_phone = normal_models.CharField(max_length=20)
	