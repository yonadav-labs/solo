from django import forms
from .models import *


class AddressForm(forms.Form):
    address = forms.CharField()
    

class OrderForm(forms.Form):
	seller_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}))
	price_unit = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}))
	thumbnail = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}))
	min_order_amount = forms.FloatField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}))
	license_number = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}))
	quantity = forms.FloatField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}))
        # widgets = {
        #     'dropoff_addr': forms.TextInput(
        #         attrs={'required': True, 'class': 'form-control'}
        #     ),
        #     'dropoff_time': forms.DateTimeInput(
        #         attrs={'required': True, 'class': 'form-control'},
        #         format='%Y-%m-%d %I:%M %p',
        #     ),        
        # }
        # labels = {
        #     'dropoff_addr': 'Drop off Address',
        #     'dropoff_time': 'Drop off Time',
        # }