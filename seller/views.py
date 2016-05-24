from urllib2 import URLError
import requests
import stripe

from django.contrib.gis import geos
from django.contrib.gis import measure
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.mail import send_mail

from geopy.geocoders import GoogleV3, Nominatim
from geopy.exc import GeocoderQueryError

from .forms import *
from .models import *
from allauth.socialaccount.models import *

def get_sellers(location):
    '''
    get sellers cover the current location and  return then in distance order
    '''
    current_point = geos.fromstr("POINT(%s)" % location)
    sellers = Seller.gis.distance(current_point).order_by('distance')
    return [seller for seller in sellers if seller.distance.mi <= seller.radius] # this is good but we also want the filter on open_hours

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
        form = AddressForm(request.POST)
        if form.is_valid():
            location2 = form.cleaned_data['address']
            sellers = get_sellers(location2)
            lnglat = location2.split(' ')
            location1 = '%s,%s' % (lnglat[1], lnglat[0])
    else:
        form = AddressForm()
        ip = get_client_ip(request) # this seems to work only onClick events
        ip = '142.33.135.231' # this is the location at which the map initializes the location, this needs to be set to the ip address of the user.
        lat, lon = get_client_location_with_ip(ip)
        location1 = '%f, %f' % (lat, lon)
        location2 = '%f %f' % (lon, lat)    # geopy location
        sellers = get_sellers(location2)

    return render(request, 'buy.html', {
        'form': form, 
        'sellers': sellers, 
        'location1': location1, 
        'location2': location2
    })

@csrf_exempt
def start_order(request):
    id = request.POST.get('id')
    location = request.POST.get('location')
    
    # geolocator = Nominatim()
    # address = geolocator.reverse(location)

    seller = Seller.objects.get(id=id)
    initial_data = model_to_dict(seller)
    #initial_data['address'] = address
    initial_data['address'] = location

    form = OrderForm(initial=initial_data)

    return render(request, 'order.html', {
        'form': form, 
        'key': settings.STRIPE_KEYS['PUBLIC_KEY']
    })


def charge(request):
    form = OrderForm(request.POST)
    if form.is_valid():
        seller_email = form.cleaned_data['email']
        seller = Seller.objects.get(email=seller_email)
        price_in_cents = int(seller.unit_price * float(form.cleaned_data['quantity']))

        card = request.POST.get('stripeToken')
        stripe.api_key = settings.STRIPE_KEYS['API_KEY']
        stripe_account_id = SocialAccount.objects.get(user__id=seller.id, provider='stripe').uid

        charge = stripe.Charge.create(
            amount=price_in_cents,
            currency="usd",
            source=card,
            destination=stripe_account_id,
            application_fee = int(price_in_cents * 0.30),
            description='Thank you for your purchase!'            
        )

        sale = Sale()
        sale.seller = seller
        sale.quantity = float(form.cleaned_data['quantity'])
        # sale.delivery_address = form.cleaned_data['address']
        sale.buyer_name = form.cleaned_data['buyer_name']
        sale.buyer_phone = form.cleaned_data['buyer_phone']
        sale.charge_id = charge.id
        sale.save()

        # send email
        email_subject = 'Order Confirmation'    
        email_body = "Dear %s.\n\nYou've got an order from Customer: %s \nPhone Number: %s\nPlease confirm the order and fulfill it.\n\nThank you." % (seller.first_name, sale.buyer_name, sale.buyer_phone)
        send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [seller.email], fail_silently=False)

        return render(request, 'order_success.html', {'seller': seller})

    return render(request, 'order.html', {
        'form': form, 
        'key': settings.STRIPE_KEYS['PUBLIC_KEY']
    })

def login(request):
	return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')    

# login required for creating new seller account
@login_required(login_url='/login')
def seller(request):
    seller = Seller.objects.get(username=request.user)

    if request.method == 'GET':
        form = SellerForm(initial=model_to_dict(seller))
    else:
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():         
            seller.address = form.cleaned_data['address']
            seller.phone = form.cleaned_data['phone']
            seller.radius = form.cleaned_data['radius']
            seller.item = form.cleaned_data['item']
            seller.unit_price = form.cleaned_data['unit_price']
            seller.picture = form.cleaned_data['picture']
            seller.description = form.cleaned_data['description']
            seller.min_order_amount = form.cleaned_data['min_order_amount']
            seller.license_number = form.cleaned_data['license_number']
            seller.license_exp = form.cleaned_data['license_exp']
            seller.save()

            return HttpResponseRedirect('/login/')

    return render(request, 'seller.html', {'form': form})
