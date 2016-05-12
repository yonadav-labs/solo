# https://www.safaribooksonline.com/library/view/lightweight-django/9781491946275/ch04.html

# templates
from django.shortcuts import render
from django.views.generic import TemplateView

# models
from models import *
from rest_framework import routers, serializers, viewsets, generics, filters
from forms import ListingForm, SalePaymentForm
from serializers import ListingSerializer
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser

from urllib2 import URLError
from django.contrib.gis import geos
from django.contrib.gis import measure
from django.shortcuts import render_to_response
from django.template import RequestContext
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError

# forms
from .forms import AddressForm


#########################################
# log in logout							#
#########################################		
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
	return render(request, 'login.html')
	
def logout(request):
	auth_logout(request)
	return redirect('/')

#home:
def home(request):
    return render(request, 'home.html')

# order screen
def order(request):
    return render(request, 'orderscreen.html')	
	
	
#def success(request):
#    return render(request, 'success.html')	
	
	
# forms
# login required for creating new seller account
@login_required(login_url='/login')
def new(request):
    tmpl_vars = {'form': ListingForm()}
    return render(request, 'app.html', tmpl_vars)

# listing
def all(request):
	return render(request, 'listing.html')

# about
def about(request):
	return render(request, 'about.html')

# detail
def detail(request):
	return render(request, 'detail.html')

	
##############################################
# views										 #
##############################################	
	
# custom template tag for verbose names
from django import template
register = template.Library()

# rest framework
router = routers.DefaultRouter()

# perform create 
import json
import urllib
from decimal import Decimal

# using class based views
# make this a function based view and grab a random value from origin and from destination?
class ListingCollection(generics.ListCreateAPIView):
	parser_classes = (FormParser, MultiPartParser)
	queryset = Listing.objects.all()
	serializer_class = ListingSerializer
	
class ListingDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Listing.objects.all()
	serializer_class = ListingSerializer
	
#############################################
# can use this for google login in login.html
"""
						<h1 class="cover-heading"></h1>
							<p class="lead">Login with Google:</p>		
							<p> <a href="{% url 'social:begin' 'google-oauth2' %}?next='/new'" class="btn btn-default">Google Login</a></p>
"""


##############################################
# stripe check out views #
# source: https://pinax-stripe.readthedocs.org/en/latest/user-guide/getting-started/
##############################################
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
 
def charge(request):
    if request.method == "POST":
        form = SalePaymentForm(request.POST)
 
        if form.is_valid(): # charges the card
            return render(request, 'success.html')
    else:
        form = SalePaymentForm()
 
    return render_to_response("checkout.html",
                        RequestContext( request, {'form': form} ) )




##############################################
# get fulfillment partner metadata #
# source: https://blog.birdhouse.org/2013/12/03/django-allauth-retrieve-firstlast-names-from-fb-twitter-google/comment-page-1/
##############################################
# When account is created via allauth, get address of seller and save to Listing module.





### map ####

	
def geocode_address(address):
    address = address.encode('utf-8')
    geocoder = GoogleV3()
    try:
        _, latlon = geocoder.geocode(address)
    except (URLError, GQueryError, ValueError):
        return None
    else:
        return latlon

def get_sellers(longitude, latitude):
    current_point = geos.fromstr("POINT(%s %s)" % (longitude, latitude))
    distance_from_point = {'mi': 10}
    sellers = Seller.gis.filter(location__distance_lte=(current_point, measure.D(**distance_from_point)))
    sellers = sellers.distance(current_point).order_by('distance')
    return sellers.distance(current_point)

def home(request):
    form = AddressForm()
    sellers = []
    if request.POST:
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            location = geocode_address(address)
            if location:
                latitude, longitude = location
                sellers = get_sellers(longitude, latitude)

    return render_to_response(
        'buyer.html', 
        {'form': form, 'sellers': sellers},
        context_instance=RequestContext(request)) 
