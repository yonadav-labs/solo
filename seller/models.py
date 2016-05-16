from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis import geos

from django.db import models as normal_models
 
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError

from urllib2 import URLError
from django.conf import settings


class Seller(normal_models.Model):
	name = normal_models.CharField(max_length=200, unique=True)
	address = normal_models.CharField(max_length=100)
	location = models.PointField(u"longitude/latitude", geography=True, blank=True, null=True)
	phone = normal_models.IntegerField(blank=True, null=True) # seems to validate less than 2147483647 and so not all phone numbers will validate
	email = normal_models.CharField(max_length=50)
	radius = normal_models.FloatField(default=10)
	open_hour = normal_models.IntegerField(default=8)
	close_hour = normal_models.IntegerField(default=6)

	item = normal_models.CharField(max_length=50)
	unit_price = normal_models.IntegerField()		# price in cent
	picture = normal_models.FileField(blank=True, null=True)
	description = normal_models.TextField(blank=True, null=True)
	min_order_amount = normal_models.IntegerField(default=1)
	license_number = normal_models.CharField(max_length=50, default='234523525342')
	license = normal_models.TextField(blank=True, null=True)
	license_exp = normal_models.DateField(blank=True, null=True)
	is_active = normal_models.BooleanField(default=True)
	operating_days = normal_models.CharField(max_length=100, blank=True, null=True) # how does this work? How do we select M-F and times for each day. How does Seller go on vacation and take a break or set status to "on-hold" for a period of time? How do we use this to show sellers to customers when they query based on location etc.?

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


 
#############################################################
# this is the charge model. 								#
# we want to include additional info about the charge, 		#
# such as fulfillment_partner_token, customer_token,		#
# amount, price, sales tax, date-time, delivery distance,	#
# date-time estimated delivery based on Google Maps API.	#
#############################################################


# sale model
class Sale(normal_models.Model):
	seller = normal_models.ForeignKey(Seller, related_name="seller")
	quantity = normal_models.FloatField()
	# store the stripe charge id for this sale
	charge_id = normal_models.CharField(max_length=32, null=True, blank=True)
	delivery_address = normal_models.CharField(max_length=100) # needs to come from Leafletjs + GeoJson or Google Maps API or Buyer form
	#delivery_lat = models.DecimalField() # this needs to come from the Leafletjs 
	#delivery_lng = models.DecimalField() # this needs to come from the Leafletjs
	#delivery_point = models.PointField() # this needs to come from the Leafletjs

	def __init__(self, *args, **kwargs):
		super(Sale, self).__init__(*args, **kwargs)

		# bring in stripe, and get the api key from settings.py
		import stripe
		stripe.api_key = settings.STRIPE_API_KEY

		self.stripe = stripe
 
	def charge(self, number, exp_month, exp_year, cvc):
		"""
		Takes a the price and credit card details: number, exp_month,
		exp_year, cvc.

		Returns a tuple: (Boolean, Class) where the boolean is if
		the charge was successful, and the class is response (or error)
		instance.
		"""
		price_in_cents = int(self.quantity * self.seller.unit_price)

		if self.charge_id: # don't let this be charged twice!
			return False, Exception(message="Already charged.")

		try:
			response = self.stripe.Charge.create(
				amount = price_in_cents,
				currency = "usd",
				card = {
				"number" : number,
				"exp_month" : exp_month,
				"exp_year" : exp_year,
				"cvc" : cvc,
				#### it is recommended to include the address! ###
				},
				#application_fee = price_in_cents * 0.30, # application fee. 
				#destination = fulfillment_partner_token # this doesn't work. need to figure out how to populate this with Seller selected by Buyer.
				#tax = need to figure this out. may be best to use Stripe third party application like Avalar or TaxCloud and let Seller handle.
				description='Thank you for your purchase!')

			self.charge_id = response.id
			#self.amount = response.amount
		except self.stripe.CardError, ce:
			# charge failed
			return False, ce

		return True, self

