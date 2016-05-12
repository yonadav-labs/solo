from django.conf.urls import patterns, url, include
import views



urlpatterns = patterns(
	'myapp.views',
	url(r'^login', 'login'),
    url(r'^new', 'new'),
	url(r'^list', 'all'),
	url(r'^about', 'about'),
	url(r'^detail', 'detail'),
	# order screen
	url(r'^order', 'order'),
	# checkout page
	url(r'^checkout', 'charge'),
	#url(r'^success', 'success'),
    # api
	url(r'^api/v1/origin/$', views.ListingCollection.as_view()),
	url(r'^api/v1/origin/(?P<pk>[0-9]+)/$', views.ListingDetail.as_view()),
) 
