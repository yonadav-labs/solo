from urllib2 import URLError

from django.contrib.gis import geos
from django.contrib.gis import measure
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError

import requests

from .forms import *
from .models import *

def get_sellers(location):
    '''
    get sellers cover the current location and  return then in distance order
    '''
    current_point = geos.fromstr("POINT(%s)" % location)
    sellers = Seller.gis.distance(current_point).order_by('distance')
    return [seller for seller in sellers if seller.distance.mi <= seller.radius] # this is good but we also want the filter on open_hours

# this doesn't seem to work correctly.
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
    '''
    get location from the ip with IP API
    '''
    url = 'http://ip-api.com/json/' + ip
    out = requests.get(url=url).json()
    return out['lat'], out['lon']

def home(request):
    if request.POST:
        form = AddressForm(request.POST)
        if form.is_valid():
            location2 = form.cleaned_data['address']
            sellers = get_sellers(location2)
            lnglat = location2.split(' ')
            location1 = '%s,%s' % (lnglat[1], lnglat[0])
    else:
        form = AddressForm()
        sellers = [] 
        ip = get_client_ip(request) # this seems to work only onClick events
        ip = '142.33.135.231' # this is the location at which the map initializes the location, this needs to be set to the ip address of the user.
        lat, lon = get_client_location_with_ip(ip)
        location1 = '%f, %f' % (lat, lon)
        location2 = '%f %f' % (lon, lat)    # geopy location

    return render(request, 'home.html', {
        'form': form, 
        'sellers': sellers, 
        'location1': location1, 
        'location2': location2
    })

@csrf_exempt
def start_order(request):
    id = request.POST.get('id')
    seller = Seller.objects.get(id=id)
    form = OrderForm(initial={'license_number':seller.license_number, 'seller_name': seller.name, 'price_unit': seller.price_unit, 'thumbnail':seller.picture, 'min_order_amount':seller.min_order_amount})

    return render(request, 'order.html', {
        'form': form, 
    })

	
# login and logout redirect	
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
	return render(request, 'login.html')
	
def logout(request):
	auth_logout(request)
	return redirect('/')	
	
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')
	
	
	
	
	
	