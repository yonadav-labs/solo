from datetime import date, datetime

from django import forms
from .models import *


class SellerForm(forms.ModelForm):
	phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}), error_messages = {'invalid': "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."}, label="Phone Number")

	class Meta:
		model = Seller
		fields = ['first_name', 'email', 'address', 'phone', 'radius', 'open_hour', 'close_hour', 'operating_days', 'estimated_delivery', 'item', 'unit_price', 'picture', 'description', 'min_order_amount', 'permit_number', 'permit_exp']		
		widgets = {
			'first_name': forms.TextInput(
				attrs={'required': True, 'class': 'form-control'}
			),
			'email': forms.TextInput(
				attrs={'readonly': True, 'class': 'form-control'}
			),
			'address': forms.TextInput(
				attrs={'required': True, 'class': 'form-control'}
			),
			'radius': forms.TextInput(
				attrs={'class': 'form-control'}
			),        
			'open_hour': forms.TextInput(
				attrs={'class': 'form-control'}
			),
			'close_hour': forms.TextInput(
				attrs={'class': 'form-control'}
			),
			'item': forms.TextInput(
				attrs={'required': True, 'class': 'form-control'}
			),            
			'unit_price': forms.TextInput(
				attrs={'required': True, 'class': 'form-control'}
			),
			'description': forms.TextInput(
				attrs={'class': 'form-control'}
			),
			'min_order_amount': forms.TextInput(
				attrs={'class': 'form-control'}
			),
			'permit_number': forms.TextInput(
				attrs={'class': 'form-control',}
			),
			'permit_exp': forms.TextInput(
				attrs={'class': 'form-control'}
			),
			'operating_days': forms.CheckboxSelectMultiple(
				attrs={'class': 'weekday'}
			),
			'estimated_delivery': forms.Select(
				choices=Estimated_Order_to_Delivery,              
				attrs={'required': True, 'class': 'form-control'}
			),
		}
		labels = {
			'first_name': 'Business Name',
			'permit_exp': 'Permit Expiration',
			'unit_price': 'Price in Dollars and Cents',
			'min_order_amount': 'Min Order Quantity of Units',
		}
	
		
class OrderForm(forms.Form):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label='Seller Name')
	email = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label='Seller Email')
	phone = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label='Seller Phone')
	distance = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label='Distance Away')
	address = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}), label='Customer Location')
	estimated_delivery = forms.CharField(widget=forms.Select(choices=Estimated_Order_to_Delivery,attrs={'readonly': True, 'class': 'form-control', 'disabled': 'disabled'}), label='Estimated Delivery Time')
	
	unit_price = forms.DecimalField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label="Unit Price in Dollars and Cents")
	min_order_amount = forms.FloatField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label="Min. Quantity of Units")	
	permit_number = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}))
	quantity = forms.FloatField(widget=forms.NumberInput(attrs={'required': True, 'class': 'form-control'}), label="Quantity of Units")
	buyer_name = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}), label="Buyer Name")
	#buyer_phone = forms.CharField(widget=forms.TextInput(attrs={'required':True, 'class': 'form-control'}), label="Buyer Phone Number:")
	buyer_phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}), error_messages = {'invalid': "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."}, label="Buyer Phone Number")

	def is_valid(self):
		# run the parent validation first
		valid = super(OrderForm, self).is_valid()
		for error in self._errors:
			if error not in ['estimated_delivery', 'unit_price']:
				return False
		return True
			  