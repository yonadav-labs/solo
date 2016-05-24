from django.conf.urls import url, patterns, include
from django.contrib.gis import admin
from seller import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^buy/', views.buy, name='buy'),
    url(r'^start_order/$', views.start_order, name='start_order'),
    url(r'^charge/$', views.charge, name="charge"),
	url(r'^login/$', views.login),
	url(r'^seller/$', views.seller),
	url(r'^about/$', views.about),
	url(r'^accounts/', include('allauth.urls')),
]
