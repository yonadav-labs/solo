from django.contrib.gis import admin
from django.contrib import admin as normal_admin
from .models import *

normal_admin.site.register(Seller)
admin.site.register(Sale)
