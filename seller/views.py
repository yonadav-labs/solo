from urllib2 import URLError

from django.contrib.gis import geos
from django.contrib.gis import measure
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict

from geopy.geocoders import GoogleV3, Nominatim
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
    location = request.POST.get('location')
    
    # geolocator = Nominatim()
    # address = geolocator.reverse(location)

    seller = Seller.objects.get(id=id)
    initial_data = model_to_dict(seller)
    # initial_data['address'] = address
    initial_data['address'] = location

    form = OrderForm(initial=initial_data)

    return render(request, 'order.html', {
        'form': form, 
    })


def pre_charge(request):
    form = OrderForm(request.POST)
    if form.is_valid():
        seller = Seller.objects.get(name=form.cleaned_data['name'])
        sale = Sale()
        sale.seller_id = seller.id
        sale.quantity = form.cleaned_data['quantity']
        sale.delivery_address = form.cleaned_data['address']
        sale.save()

        saleform = SalePaymentForm(initial={'sale_id':sale.id})
        return render(request, "checkout.html", {'form': saleform})
    return render(request, 'order.html', {
        'form': form, 
    })

def charge(request):
    if request.method == "POST":
        form = SalePaymentForm(request.POST)
 
        if form.is_valid(): # charges the card
            return HttpResponse("Success! We've charged your card!")
 
    return render(request, "checkout.html",
                        {'form': form})

# login and logout redirect	
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
	return render(request, 'login.html')
	
def logout(request):
#Add a comment to this line
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

# login required for creating new seller account
@login_required(login_url='/login')
def seller(request):
    tmpl_vars = {'form': AddressForm()}
    return render(request, 'seller.html', tmpl_vars)	
						