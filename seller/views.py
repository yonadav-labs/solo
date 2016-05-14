from urllib2 import URLError

from django.contrib.gis import geos
from django.contrib.gis import measure
from django.shortcuts import render
from django.template import RequestContext

from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError

import requests

from .forms import *
from .models import *

def get_sellers(location):
    current_point = geos.fromstr("POINT(%s)" % location)
    sellers = Seller.gis.distance(current_point).order_by('distance')
    return [seller for seller in sellers if seller.distance.mi <= seller.radius]

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_location_with_ip(ip):
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
        ip = get_client_ip(request)
        ip = '142.33.135.231'
        lat, lon = get_client_location_with_ip(ip)
        location1 = '%f, %f' % (lat, lon)
        location2 = '%f %f' % (lon, lat)    # geopy location

    return render(request, 'home.html', {
        'form': form, 
        'sellers': sellers, 
        'location1': location1, 
        'location2': location2
    })
