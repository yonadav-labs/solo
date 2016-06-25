from urllib2 import URLError
from datetime import datetime
import requests
import stripe
import pytz

from django.contrib.gis import geos
from django.contrib.gis import measure
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from geopy.geocoders import GoogleV3, Nominatim
from geopy.exc import GeocoderQueryError

from .forms import *
from .models import *
from allauth.socialaccount.models import *

def get_sellers(location):
	'''
	get open and shortest delivery hour
	get sellers cover the current location and  return then in distance order
	'''
	utc_now = timezone.now()

	# filter workday and time in local time
	sellers_id = []
	for seller in Seller.objects.all():
		if not (seller.time_zone and seller.is_active):
			continue
		local_timezone = pytz.timezone(seller.time_zone)
		local_time = utc_now.astimezone(local_timezone)
		weekday = local_time.isoweekday()

		if seller.operating_days.filter(id=weekday) and local_time.time() > seller.open_hour and local_time.time() < seller.close_hour:
			sellers_id.append(seller.id)

	current_point = geos.fromstr("POINT(%s)" % location)
	dis_sellers = Seller.gis.distance(current_point)
	# sort by estimated delivery time    
	dis_sellers = dis_sellers.filter(id__in=sellers_id).order_by('estimated_delivery') 
	# filter only in radius
	sellers = [seller for seller in dis_sellers if seller.distance.mi <= seller.radius]
	return sellers

def get_client_ip(request):
	'''
	get ip from the request
	'''
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[-1].strip()
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def get_client_location_with_ip(ip):
	FREEGEOPIP_URL = 'http://freegeoip.net/json'
	url = '{}/{}'.format(FREEGEOPIP_URL, ip)

	response = requests.get(url)
	response.raise_for_status()
	out = response.json()

	return out['latitude'], out['longitude']

def home(request):
	return render(request, 'landing.html')

def buy(request):    
	if request.POST:
		location2 = request.POST['address']
		# print '@@@@@', location2
		lnglat = location2.split(' ')
		location1 = '%s,%s' % (lnglat[1], lnglat[0])
		sellers = get_sellers(location2)
		return render(request, 'buy.html', { 
			'sellers': sellers,
			'location1': location1,
			'location2': location2 })
	else:
		return render(request, 'buy.html', { 'map_initial': True })

@csrf_exempt
def start_order(request):
	id = request.POST.get('id')
	location = request.POST.get('location')
	distance = request.POST.get('distance')
	geolocator = Nominatim()
	address = geolocator.reverse(location)

	seller = Seller.objects.get(id=id)
	initial_data = model_to_dict(seller)
	initial_data['address'] = address
	initial_data['unit_price'] = '$'+str(initial_data['unit_price']) 
	# initial_data['address'] = location
	initial_data['distance'] = distance+' miles away'

	form = OrderForm(initial=initial_data)

	return render(request, 'order.html', {
		'form': form, 
		'key': settings.STRIPE_KEYS['PUBLIC_KEY']
	})


def get_tax(address, price):
	'''
	calculate tax from address
	accept only usa now
	Avalara TaxRatesAPI key. Free and limits requests to 15 per minute 
	resources: http://taxratesapi.avalara.com/docs	
	'''
	tax = 0
	address = address.split(',')	
	country = address[-1].strip()
	if country == 'United States of America':
	# if country == 'Canada':
		postal = address[-2].strip()

		key = 'RjCqBdo2dxlGbTNWyo3uxsf8xv+T/teMcaL9TN6DhNy49DmC1nzbJ7QFIxjb6IjTkcrWVxo186CUhB/zs+AC4A=='
		url = 'https://taxrates.api.avalara.com:443/postal?country=%s&postal=%s' % ('usa', postal)

		header = {"Authorization": "AvalaraApiKey "+key}
		res = requests.get(url=url, headers=header)
		res_json = res.json()
		tax = float(res_json.get('totalRate', 0.0))
		tax = int(price * tax / 100) 
	return tax

def charge(request):
	form = OrderForm(request.POST)
	if form.is_valid():
		seller_email = form.cleaned_data['email']
		seller = Seller.objects.get(email=seller_email)
		price_in_cents = int(int(seller.unit_price * 100) * float(form.cleaned_data['quantity']))
		card = request.POST.get('stripeToken')
		stripe.api_key = settings.STRIPE_KEYS['API_KEY']
		stripe_account_id = SocialAccount.objects.get(user__id=seller.id, provider='stripe').uid
	
		tax = get_tax(form.cleaned_data['address'], price_in_cents)	
		# tax = 0
		charge = stripe.Charge.create(
			amount=price_in_cents+tax,
			currency="usd",
			source=card,
			destination=stripe_account_id,
			application_fee = int(price_in_cents * 0.30),
			description='Thank you for your purchase!'
		)
		
		sale = Sale()
		sale.seller = seller
		sale.quantity = float(form.cleaned_data['quantity'])
		sale.delivery_address = form.cleaned_data['address']
		sale.buyer_name = form.cleaned_data['buyer_name']
		sale.buyer_phone = form.cleaned_data['buyer_phone']
		sale.charge_id = charge.id
		sale.save()
		
		# send email
		email_subject = 'Order Confirmation'
		email_body = "Dear %s.\n\nYou've got an order from Customer: %s \nAddress: %s\nPhone Number: %s\nQuantity: %.2f\nPlease confirm the order and fulfill it.\n\nThank you." % (seller.first_name, sale.buyer_name, sale.delivery_address, sale.buyer_phone, sale.quantity)
		send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [seller.email], fail_silently=False)
		
		return render(request, 'order_success.html', {'seller': seller})
	return render(request, 'order.html', {
		'form': form,
		'key': settings.STRIPE_KEYS['PUBLIC_KEY']
	})

def login(request):
	return render(request, 'login.html')

def about(request):
	# return render(request, 'about.html', {'timezones': pytz.common_timezones})    
	return render(request, 'about.html')    

# login required for creating new seller account
@login_required(login_url='/login/')
def seller(request):
	seller = Seller.objects.get(username=request.user)

	if request.method == 'GET':
		form = SellerForm(initial=model_to_dict(seller))
	else:
		form = SellerForm(request.POST, request.FILES)
		if form.is_valid():         
			seller.first_name = form.cleaned_data['first_name']
			seller.open_hour = form.cleaned_data['open_hour']
			seller.close_hour = form.cleaned_data['close_hour']
			seller.address = form.cleaned_data['address']
			seller.phone = form.cleaned_data['phone']
			seller.radius = form.cleaned_data['radius']
			seller.item = form.cleaned_data['item']
			seller.unit_price = form.cleaned_data['unit_price']
			if form.cleaned_data['picture']:
				seller.picture = form.cleaned_data['picture']
			seller.description = form.cleaned_data['description']
			seller.min_order_amount = form.cleaned_data['min_order_amount']
			seller.permit_number = form.cleaned_data['permit_number']
			seller.permit_exp = form.cleaned_data['permit_exp']
			# seller.license = form.cleaned_data['license']
			seller.operating_days = form.cleaned_data['operating_days']
			seller.estimated_delivery = form.cleaned_data['estimated_delivery']
			seller.save()

			return HttpResponseRedirect('/login/')

	open_hour = seller.open_hour.hour * 60 + seller.open_hour.minute
	close_hour = seller.close_hour.hour * 60 + seller.close_hour.minute

	return render(request, 'seller.html', {'form': form, 'open_hour': open_hour, 'close_hour': close_hour })

	
# def handler404(request):
# 	response = render_to_response('404.html', {}, context_instance=RequestContext(request))
# 	response.status_code = 404
# 	print '@@@@@@@@@ 404'
# 	return response
	
# def handler500(request):
# 	response = render_to_response('500.html', {}, context_instance=RequestContext(request))
# 	response.status_code=500
# 	print '@@@@@@@@@ 500'
# 	return response
	
	
	