### stripe payment example
### https://github.com/bryanhelmig/django-stripe-example/blob/master/sales/models.py


"""

simple. local. independent. craft. original. made with care.
one flavor choice.
one random monthly flavor choice. baker's special.
quantity choices.
fullfilled by local partners.
local partners chosen to fulfill based on proximity and based on availability.
if not available, then return message to customer saying not available and inviting them to be a fulfillment partner.
application for fulfullment partner = license uploaded and date and name and address and phone number and expiration date entered into a form.
when approaching expiration, signal an email to fulfillment partner and to admin to follow up.
Admin can remove fulfillment partner at will.
customer can provide feedback. an email needs to be sent to customer to request their feedback. about each fulfillment partner. 
fulfillment partner which receives poor ratings are put on warning and then removed if not satisfactory rating or review by admin. 
need an independent contractor agreement about this too. so will need a legal agreement for fulfillment partner to agree to before final submition of
their application.

"""

from __future__ import unicode_literals
from django.db import models
from decimal import Decimal
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator # source: http://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models

from urllib2 import URLError

from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError
#########################################################
# created choices but not using them in views yet.		#
# may not need to do it this way. This represents 		#
# quantity of orders.									#
#														#
#########################################################

QUANTITY_CHOICES = (
	('0', '0'),
	('1', '1'),
	('2', '2'),
	('3', '3'),
	('4', '4'),
	('5', '5'),
	('6', '6'),
	('8', '8'),
	('9', '9'),
	('10', '10'),
	('11', '11'),
	('12', '12'),
	('13', '13'),
	('14', '14'),
	('15', '15'),
	('16', '16'),
	('17', '17'),
	('18', '18'),
	('19', '19'),
	('20', '20'),
)


#############################################################
# Default should be "Not Active" and only Admin can 		#
# change to "Active" from Admin page. This is changed to	#
# "Active" once Admin reviews fulfillment partner 			#
# application and approves to sell for brand.				#
#															#
#############################################################


ACTIVE_CHOICES = (
	('Active', 'Active'),
	('Not Active', 'Not Active'),
)

#############################################################
# Default should be "Active". This is so fulfillment partner#
# can select themselves as "Not Active" so they can go on 	#
# vacation or take a period of time from fulfilling orders. #
#															#
#############################################################

TEMP_INACTIVE_CHOICES = (
	('Active', 'Active'),
	('Not Active', 'Not Active'),
)


#############################################################
# this is the fulfillment partner model. It is the Seller. 	#
# The seller initially signs in with Stripe Connect, so any	#
# pre-filled attributes which are in the response can be	#
# automatically included									#
#															#
#############################################################


# subclass user to include additional information if possible.
# allow anyone to be a fulfillment partner so keep it in the same model, but add an approved flag and an active flag, and an upload for license image
# GeoDjango source: http://stackoverflow.com/questions/11421230/django-how-do-i-store-a-geo-point-in-database
class Listing(models.Model):
	fulfillment_partner = models.OneToOneField(User, unique=True) # user id from stripe account
	address = models.CharField(max_length=100) # address of business
	active = models.CharField(max_length=20, choices=ACTIVE_CHOICES, default='Not Active') 
	#temp_active = models.CharField(max_length=20, choices=TEMP_INACTIVE_CHOICES, default='Active') 
	#licenseImg = models.FileField() # upload pdf, jpeg, or png of license. Need filesize limits. 
	#licenseNum = models.CharField(max_length=100) # license number 
	#licenseExp = models.DateField() # license expiration date field. 
	#email = models.EmailField() # email address for fulfillment partner. I think this is stored in allauth already and comes from Stripe so may not need.
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(max_length=12 ,validators=[phone_regex], blank=True) # validators should be a list
	radius = models.IntegerField(default=10) # fulfillment partner sets this radius (in miles) in sign up and it is applied to the query which returns when customer searches. Should not allow for radius > 10 miles. We want many hyper local fulfillment partners.
	#latitude = models.DecimalField(max_digits=8, decimal_places=3) # this needs to be created from the initial save by user, from the address provided
	#longitude = models.DecimalField(max_digits=8, decimal_places=3) # this needs to be created from the initial save by the user, from the address provided
	#point = models.PointField(srid=4326, dim=3) # this needs to be created upon initial save by user, from the address provided and subsequent lat lng values
	#accuracy = models.FloatField(default=0.0)
	objects = models.GeoManager()


#############################################################
# this is the charge model. 								#
# we want to include additional info about the charge, 		#
# such as fulfillment_partner_token, customer_token,		#
# amount, price, sales tax, date-time, delivery distance,	#
# date-time estimated delivery based on Google Maps API.	#
#############################################################


# sale model
class Sale(models.Model):
    def __init__(self, *args, **kwargs):
        super(Sale, self).__init__(*args, **kwargs)
 
        # bring in stripe, and get the api key from settings.py
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY # from config.py 
 
        self.stripe = stripe
 
    # store the stripe charge id for this sale
	charge_id = models.CharField(max_length=32)
	#address = models.CharField(max_length=100)
	
	def charge(self, price_in_cents, number, exp_month, exp_year, cvc):
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
 
        return True, response

class Seller(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=100)
	phone = models.IntegerField()
	email = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	location = gis_models.PointField(u"longitude/latitude", geography=True, blank=True, null=True)
	gis = gis_models.GeoManager()
	objects = models.Manager()
	radius = models.IntegerField(default=10)
	open_hour = models.IntegerField()
	close_hour = models.IntegerField()
	item = models.CharField(max_length=50)
	item_unit = models.CharField(max_length=50)
	price_unit = models.CharField(max_length=50)
	picture = models.FileField()
	description = models.TextField()
	min_order_amount = models.IntegerField()
	license = models.TextField()
	license_exp = models.DateField()
	is_active = models.BooleanField()
	operating_days = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.name
		
	def save(self, **kwargs):
		if not self.location:
			address = u'%s %s' % (self.city, self.address)
			address = address.encode('utf-8')
			geocoder = GoogleV3()
			try:
				_, latlon = geocoder.geocode(address)
			except (URLError, GQueryError, ValueError):
				pass
			else:
				point = "POINT(%s %s)" % (latlon[1], latlon[0])
				self.location = geos.fromstr(point)
		super(Seller, self).save()        
        
