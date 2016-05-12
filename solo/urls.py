"""solo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, patterns, include
from django.contrib import admin
# from myapp.views import  login, logout, new, map, home
from myapp.views import  login, logout, new, home
#from views import logout_page
import settings


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url('', include('social.apps.django_app.urls', namespace='social')),
	url(r'^login/$', login),
	url(r'^$', home), # home site
	url(r'^logout/$', logout),
	url(r'^accounts/', include('allauth.urls')),
	url(r'', include('myapp.urls')),

] 

						 
						 

